import socket
import struct
import threading
import time
import binascii

class DSUServer:
    def __init__(self, ip="127.0.0.1", port=26760):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))
        self.running = False
        self.thread = None
        self.clients = {} # (ip, port) -> last_seen
        self.state = {}
        self.server_id = 12345678

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_server)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.sock.close()

    def update(self, state):
        self.state = state

    def _run_server(self):
        print(f"DSU Server listening on {self.ip}:{self.port}")
        self.sock.settimeout(0.1)
        while self.running:
            try:
                data, addr = self.sock.recvfrom(1024)
                self._handle_packet(data, addr)
            except socket.timeout:
                pass
            except Exception as e:
                print(f"DSU Error: {e}")

    def _handle_packet(self, data, addr):
        # Basic DSU Protocol Implementation
        # Header: 'DSUS', Protocol Ver (2), Packet Len (2), CRC32 (4), Client ID (4), Msg Type (4)
        if len(data) < 16: return
        
        magic = data[0:4]
        if magic != b'DSUS': return

        msg_type = struct.unpack('<I', data[12:16])[0]

        if msg_type == 0x100000: # Protocol Version Info
            self._send_version_info(addr)
        elif msg_type == 0x100001: # Controller Info
            self._send_controller_info(addr, data)
        elif msg_type == 0x100002: # Controller Data
            self._send_controller_data(addr, data)

    def _send_version_info(self, addr):
        # Resp: Header + Version(2)
        payload = struct.pack('<H', 1001)
        self._send_response(addr, 0x100000, payload)

    def _send_controller_info(self, addr, request):
        # Slot (1), Slot State (1), Device Model (1), Connection (1), MAC (6), Battery (1)
        # Slot 0 is our HOTAS
        slot = request[16]
        if slot != 0: return # Only support slot 0

        payload = struct.pack('<BBBBBBBBBB', 
            0, # Slot
            2, # Connected
            2, # Model: DS4
            2, # Connection: USB
            0x00, 0x00, 0x00, 0x00, 0x00, 0x01, # MAC
            0x05, # Battery: Full
            0x00 # Term
        )
        self._send_response(addr, 0x100001, payload)

    def _send_controller_data(self, addr, request):
        slot = request[16]
        if slot != 0: return

        # Packet format:
        # Slot(1), State(1), Model(1), Conn(1), MAC(6), Battery(1), Active(1), PacketNo(4), 
        # Buttons(2), PS Button(1), Touch(1), Left Stick(3), Right Stick(3), Analog DPAD(4), Analog Buttons(12), Motion(36), Touch(19)
        
        # Map state to DSU
        # Buttons: 16 bits
        # Bit 0-3: Share, L3, R3, Options
        # Bit 4-7: D-Pad (Up, Right, Down, Left)
        # Bit 8-11: L2, R2, L1, R1
        # Bit 12-15: Triangle, Circle, Cross, Square
        
        # Current 'buttons' from InputReader is a raw bitmask from the device.
        # We need to map it to DSU buttons.
        # Let's assume a simple mapping for now, similar to BrowserBridge.
        
        btn1 = self.state.get('buttons', 0)
        thr_btns = self.state.get('thr_buttons', 0)
        
        # Helper
        def is_pressed(mask, val):
            return (val & mask) > 0
            
        dsu_buttons = 0x0000
        
        # Load Mapping
        import json
        import os
        MAPPING = {}
        try:
            if os.path.exists('button_mapping.json'):
                with open('button_mapping.json', 'r') as f:
                    MAPPING = json.load(f)
        except:
            pass
            
        # Default Fallback
        if not MAPPING:
             MAPPING = {
                'A': ['joy', 0x01], 'B': ['joy', 0x02], 'X': ['joy', 0x04], 'Y': ['joy', 0x08],
                'LB': ['joy', 0x40], 'RB': ['joy', 0x100],
                'Back': ['thr', 0x00800000], 'Start': ['thr', 0x02000000], 'Guide': ['thr', 0x00400000],
                'L3': ['thr', 0x00100000], 'R3': ['thr', 0x00000001]
            }

        # DSU Protocol Button Definitions
        DSU_MAP = {
            'A': 0x4000,      # Cross
            'B': 0x2000,      # Circle
            'X': 0x8000,      # Square
            'Y': 0x1000,      # Triangle
            'LB': 0x0400,     # L1
            'RB': 0x0800,     # R1
            'Back': 0x0001,   # Share
            'Start': 0x0008,  # Options
            'Guide': 0x0010,  # PS
            'L3': 0x0002,     # L3
            'R3': 0x0004      # R3
        }

        joy_btns = self.state.get('buttons', 0)
        thr_btns = self.state.get('thr_buttons', 0)

        for btn_name, dsu_mask in DSU_MAP.items():
            if btn_name in MAPPING:
                val_data = MAPPING[btn_name]
                source = val_data[0]
                mask = val_data[1]
                val = joy_btns if source == 'joy' else thr_btns
                
                if (val & mask) > 0:
                    dsu_buttons |= dsu_mask
        
        # L2 (0x0100), R2 (0x0200) - Digital triggers (Keep these separate as they are axes)
        if self.state.get('throttle_left', 0) > 0.5: dsu_buttons |= 0x0100
        if self.state.get('throttle_right', 0) > 0.5: dsu_buttons |= 0x0200

        # D-Pad (Hat)
        # DSU D-Pad: Up(0x10), Right(0x20), Down(0x40), Left(0x80)
        hat = self.state.get('hat', -1)
        if hat == 0 or hat == 1 or hat == 7: dsu_buttons |= 0x0010 # Up
        if hat == 1 or hat == 2 or hat == 3: dsu_buttons |= 0x0020 # Right
        if hat == 3 or hat == 4 or hat == 5: dsu_buttons |= 0x0040 # Down
        if hat == 5 or hat == 6 or hat == 7: dsu_buttons |= 0x0080 # Left

        # Axes: 0-255. 128 is center.
        # Joy X/Y (-1.0 to 1.0) -> 0-255
        lx = int((self.state.get('joy_x', 0) + 1.0) * 127.5)
        ly = int((self.state.get('joy_y', 0) + 1.0) * 127.5)
        
        # Right Stick (Slew)
        rx = int((self.state.get('slew_x', 0) + 1.0) * 127.5)
        ry = int((self.state.get('slew_y', 0) + 1.0) * 127.5)

        # Throttle -> L2/R2 (0-255)
        l2 = int(self.state.get('throttle_left', 0) * 255)
        r2 = int(self.state.get('throttle_right', 0) * 255)

        payload = bytearray()
        payload.append(0) # Slot
        payload.append(2) # Connected
        payload.append(2) # Model DS4
        payload.append(2) # USB
        payload.extend([0,0,0,0,0,1]) # MAC
        payload.append(5) # Battery
        payload.append(1) # Active
        payload.extend(struct.pack('<I', int(time.time() * 1000))) # Packet No
        
        payload.extend(struct.pack('<H', dsu_buttons))
        payload.append(0) # PS Button
        payload.append(0) # Touch

        payload.append(lx)
        payload.append(ly)
        payload.append(rx)
        payload.append(ry)
        
        payload.extend([0]*4) # Analog DPAD
        payload.append(l2) # L2
        payload.append(r2) # R2
        payload.extend([0]*10) # Other analog buttons

        # Motion (Accel/Gyro) - Zeroed
        payload.extend(struct.pack('<ffffff', 0,0,0,0,0,0))
        
        # Touch Data - Zeroed
        payload.extend([0]*19)

        self._send_response(addr, 0x100002, payload)

    def _send_response(self, addr, msg_type, payload):
        # Header: 'DSUS', Ver(2), Len(2), CRC(4), ID(4), Type(4)
        header = bytearray(b'DSUS')
        header.extend(struct.pack('<H', 1001))
        length = len(payload) + 4 # Payload + CRC? No, just payload usually, but protocol varies. 
        # Actually DSU protocol length includes header? No.
        # Let's assume standard implementation.
        
        # Construct full packet first to calc CRC
        # Wait, CRC is part of header.
        
        # Packet: Header + Payload
        # Header CRC is 0 initially
        
        pkt = bytearray(b'DSUS')
        pkt.extend(struct.pack('<H', 1001))
        pkt.extend(struct.pack('<H', len(payload)))
        pkt.extend(struct.pack('<I', 0)) # CRC placeholder
        pkt.extend(struct.pack('<I', self.server_id))
        pkt.extend(struct.pack('<I', msg_type))
        pkt.extend(payload)

        # Calc CRC32
        crc = binascii.crc32(pkt) & 0xffffffff
        struct.pack_into('<I', pkt, 8, crc)

        self.sock.sendto(pkt, addr)
