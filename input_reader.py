import hid
import struct
import threading
import time

class InputReader:
    VENDOR_ID = 0x044f
    JOYSTICK_ID = 0x0402
    THROTTLE_ID = 0x0404

    def __init__(self):
        self.joystick = None
        self.throttle = None
        self.running = False
        self.state = {
            'joy_x': 0.0, # -1.0 to 1.0
            'joy_y': 0.0, # -1.0 to 1.0
            'throttle_left': 0.0, # 0.0 to 1.0
            'throttle_right': 0.0, # 0.0 to 1.0
            'buttons': [] # List of active button IDs
        }
        self.lock = threading.Lock()

    def start(self):
        self.running = True
        # self._connect() # Moved to thread
        self.thread = threading.Thread(target=self._read_loop)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        # Closing handled in thread loop or here if needed, but better in thread cleanup
        pass

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
            print(f"Failed to connect {name}: {e}")
            return None

    def _read_loop(self):
        # Connect in the same thread
        self.joystick = self._connect_device(self.VENDOR_ID, self.JOYSTICK_ID, "Joystick")
        self.throttle = self._connect_device(self.VENDOR_ID, self.THROTTLE_ID, "Throttle")

        while self.running:
            if self.joystick:
                try:
                    data = self.joystick.read(64)
                    if data:
                        # DEBUG: Print raw data occasionally to verify offsets
                        # if time.time() % 1.0 < 0.05:
                        #    print(f"JOY RAW: {data[:16]}")
                        self._parse_joystick(data)
                except Exception as e:
                    # print(f"Joystick read error: {e}")
                    pass # Suppress spam
            
            if self.throttle:
                try:
                    data = self.throttle.read(64)
                    if data:
                        # DEBUG: Print raw throttle data
                        if time.time() % 1.0 < 0.1: # Limit spam
                           print(f"THR RAW: {[hex(x) for x in data[:12]]}")
                        self._parse_throttle(data)
                except Exception as e:
                    # print(f"Throttle read error: {e}")
                    pass
            
            time.sleep(0.005) # 200Hz
        
        # Cleanup
        if self.joystick: self.joystick.close()
        if self.throttle: self.throttle.close()

    def _parse_joystick(self, data):
        # DEBUG: Print raw hex to debug jitter and hat switch
        # print(f"JOY RAW: {[hex(x) for x in data[:12]]}")
        
        # Bytes 0: Report ID
        # Bytes 1-2: Buttons
        # Byte 3: Hat Switch (0xF0 = Center, 0x00=Up, 0x02=Right, etc.)
        # Bytes 4-5: X Axis (16-bit little endian)
        # Bytes 6-7: Y Axis (16-bit little endian)

        # Parse Buttons
        buttons_1 = data[1]
        buttons_2 = data[2]

        # Parse Hat
        # Standard HID Hat: 0=Up, 1=UpRight, 2=Right, 3=DownRight, 4=Down, 5=DownLeft, 6=Left, 7=UpLeft
        # Warthog might use 0, 2, 4, 6 for main directions.
        hat_raw = data[3]
        hat_val = -1
        
        # Check if Hat is centered (usually 0xF0 or 0x0F or 0x80 depending on implementation)
        # Based on logs, 0xF0 seems to be the resting state.
        if (hat_raw & 0xF0) == 0xF0:
            hat_val = -1
        else:
            hat_val = hat_raw & 0x0F

        # Parse Axes
        # Little Endian: Low Byte, High Byte
        raw_x = (data[5] << 8) | data[4]
        raw_y = (data[7] << 8) | data[6]

        # Normalize to -1.0 to 1.0
        # 0x0000 = 0, 0x8000 = 32768 (Center), 0xFFFF = 65535
        norm_x = (raw_x - 32768) / 32768.0
        norm_y = (raw_y - 32768) / 32768.0

        # Clamp
        norm_x = max(-1.0, min(1.0, norm_x))
        norm_y = max(-1.0, min(1.0, norm_y))

        with self.lock:
            self.state['joy_x'] = norm_x
            self.state['joy_y'] = norm_y
            self.state['buttons_1'] = buttons_1
            self.state['buttons_2'] = buttons_2
            self.state['hat'] = hat_val

    def _parse_throttle(self, data):
        # Throttle Data (12 bytes)
        # Byte 0: Report ID
        # Bytes 1-5: Buttons/Switches/Hat
        # Bytes 6-7: Left Throttle (16-bit Little Endian, but effectively 10-bit range 0-1023?)
        # Bytes 8-9: Right Throttle (16-bit Little Endian)
        
        # Parse Axes
        # Little Endian
        raw_left = (data[7] << 8) | data[6]
        raw_right = (data[9] << 8) | data[8]
        
        # Normalize
        # Observed range: ~75 to ~631, Center ~512.
        # This suggests a 10-bit axis (0-1023) or similar.
        # Let's normalize 0-1023 to 0.0-1.0.
        # If values exceed 1023, it will clamp.
        
        norm_l = raw_left / 1023.0
        norm_r = raw_right / 1023.0
        
        # Clamp
        norm_l = max(0.0, min(1.0, norm_l))
        norm_r = max(0.0, min(1.0, norm_r))
        
        with self.lock:
            self.state['throttle_left'] = norm_l
            self.state['throttle_right'] = norm_r
