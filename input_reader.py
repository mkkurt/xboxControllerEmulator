import hid
import struct
import threading
import time

class InputReader:
    VENDOR_ID = 0x044f
    JOYSTICK_ID = 0x0402
    THROTTLE_ID = 0x0404

    # Default Mappings (can be tweaked)
    MAPPING = {
        'joystick': {
            'x': {'offset': 4, 'size': 2, 'signed': False, 'min': 0, 'max': 65535, 'center': 32768, 'deadzone': 0.05},
            'y': {'offset': 6, 'size': 2, 'signed': False, 'min': 0, 'max': 65535, 'center': 32768, 'deadzone': 0.05},
        },
        'throttle': {
            'slew_x': {'offset': 6, 'size': 2, 'min': 0, 'max': 1023, 'center': 512, 'deadzone': 0.05},
            'slew_y': {'offset': 8, 'size': 2, 'min': 0, 'max': 1023, 'center': 512, 'deadzone': 0.05},
            'left': {'offset': 14, 'size': 2, 'min': 0, 'max': 16383, 'center': None, 'deadzone': 0.01},
            'right': {'offset': 12, 'size': 2, 'min': 0, 'max': 16383, 'center': None, 'deadzone': 0.01}
        }
    }

    def __init__(self):
        self.joystick = None
        self.throttle = None
        self.running = False
        self.state = {
            'joy_x': 0.0, # -1.0 to 1.0
            'joy_y': 0.0, # -1.0 to 1.0
            'slew_x': 0.0, # -1.0 to 1.0
            'slew_y': 0.0, # -1.0 to 1.0
            'throttle_left': 0.0, # 0.0 to 1.0
            'throttle_right': 0.0, # 0.0 to 1.0
            'buttons': 0, # Joystick Buttons
            'thr_buttons': 0, # Throttle Buttons
            'hat': -1
        }
        self.lock = threading.Lock()
        self.debug_mode = False # Enable to print raw data

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._read_loop)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def get_state(self):
        with self.lock:
            return self.state.copy()

    def _connect_device(self, vendor_id, product_id, name):
        try:
            dev = hid.device()
            dev.open(vendor_id, product_id)
            dev.set_nonblocking(True)
            print(f"{name} connected.")
            return dev
        except Exception as e:
            # print(f"Failed to connect {name}: {e}")
            return None

    def _read_loop(self):
        self.joystick = self._connect_device(self.VENDOR_ID, self.JOYSTICK_ID, "Joystick")
        self.throttle = self._connect_device(self.VENDOR_ID, self.THROTTLE_ID, "Throttle")

        while self.running:
            if self.joystick:
                try:
                    data = self.joystick.read(64)
                    if data:
                        # DEBUG: Print raw joystick data periodically
                        if self.debug_mode and time.time() % 2.0 < 0.05:
                           print(f"JOY RAW: {[hex(x) for x in data[:16]]}")
                        self._parse_joystick(data)
                except Exception:
                    pass
            
            if self.throttle:
                try:
                    data = self.throttle.read(64)
                    if data:
                        # DEBUG: Print raw throttle data periodically
                        if self.debug_mode and time.time() % 2.0 < 0.05:
                           print(f"THR RAW: {[hex(x) for x in data[:16]]}")
                        self._parse_throttle(data)
                except Exception:
                    pass
            
            time.sleep(0.005) # 200Hz
        
        if self.joystick: self.joystick.close()
        if self.throttle: self.throttle.close()

    def _parse_joystick(self, data):
        # Bytes 0: Report ID
        # Bytes 1-2: Buttons
        # Byte 3: Hat Switch
        # Bytes 4-5: X Axis
        # Bytes 6-7: Y Axis

        # Parse Buttons (Simple bitmask for now)
        buttons = (data[2] << 8) | data[1]

        # Parse Hat
        # Warthog Hat seems to be in the High Nibble (0x00=Up, 0x20=Right, 0x40=Down, 0x60=Left)
        # 0xF0 is Neutral.
        hat_raw = data[3]
        hat_dir = (hat_raw >> 4) & 0x0F # Shift right 4 bits to get 0-15
        
        if hat_dir > 7: # 8-15 are neutral/unused (0xF is typical neutral)
            hat_val = -1
        else:
            hat_val = hat_dir

        # Parse Axes using Mapping
        map_x = self.MAPPING['joystick']['x']
        map_y = self.MAPPING['joystick']['y']

        raw_x = self._read_axis(data, map_x['offset'], map_x['size'])
        raw_y = self._read_axis(data, map_y['offset'], map_y['size'])

        norm_x = self._normalize(raw_x, map_x['min'], map_x['max'], map_x['center'], map_x['deadzone'])
        norm_y = self._normalize(raw_y, map_y['min'], map_y['max'], map_y['center'], map_y['deadzone'])

        with self.lock:
            self.state['joy_x'] = norm_x
            self.state['joy_y'] = norm_y
            self.state['buttons'] = buttons
            self.state['hat'] = hat_val

    def _parse_throttle(self, data):
        # Throttle Data
        # Byte 0: Report ID
        # Bytes 1-5: Buttons (5 bytes of buttons!)
        # Bytes 6-7: Slew X
        # Bytes 8-9: Slew Y
        # Bytes 10-11: ?
        # Bytes 12-13: Left Throttle
        # Bytes 14-15: Right Throttle

        # Parse Buttons
        # Combine bytes 1-5 into a large integer
        thr_buttons = 0
        for i in range(5):
            if 1 + i < len(data):
                thr_buttons |= (data[1 + i] << (8 * i))

        map_sx = self.MAPPING['throttle']['slew_x']
        map_sy = self.MAPPING['throttle']['slew_y']
        map_l = self.MAPPING['throttle']['left']
        map_r = self.MAPPING['throttle']['right']

        raw_sx = self._read_axis(data, map_sx['offset'], map_sx['size'])
        raw_sy = self._read_axis(data, map_sy['offset'], map_sy['size'])
        raw_l = self._read_axis(data, map_l['offset'], map_l['size'])
        raw_r = self._read_axis(data, map_r['offset'], map_r['size'])

        norm_sx = self._normalize(raw_sx, map_sx['min'], map_sx['max'], map_sx['center'], map_sx['deadzone'])
        norm_sy = self._normalize(raw_sy, map_sy['min'], map_sy['max'], map_sy['center'], map_sy['deadzone'])
        
        # Throttle is 0-16383, normalize to 0.0-1.0
        # Invert so that full throttle = 1.0 (not 0.0)
        norm_l = max(0.0, min(1.0, 1.0 - (raw_l / 16383.0)))
        norm_r = max(0.0, min(1.0, 1.0 - (raw_r / 16383.0)))
        
        with self.lock:
            self.state['slew_x'] = norm_sx
            self.state['slew_y'] = norm_sy
            self.state['throttle_left'] = norm_l
            self.state['throttle_right'] = norm_r
            self.state['thr_buttons'] = thr_buttons

    def _read_axis(self, data, offset, size):
        if offset + size > len(data):
            return 0
        val = 0
        for i in range(size):
            val |= (data[offset + i] << (8 * i))
        return val

    def _normalize(self, val, min_val, max_val, center, deadzone):
        # Center the value
        val -= center
        
        # Apply deadzone
        if abs(val) < (max_val - min_val) * deadzone:
            return 0.0
            
        # Normalize to -1.0 to 1.0
        if val > 0:
            return min(1.0, val / (max_val - center))
        else:
            return max(-1.0, val / (center - min_val))
