import hid
import time
import struct

VENDOR_ID = 0x044f
JOYSTICK_ID = 0x0402
THROTTLE_ID = 0x0404

def main():
    try:
        joystick = hid.device()
        joystick.open(VENDOR_ID, JOYSTICK_ID)
        joystick.set_nonblocking(True)
        print("Joystick opened")
    except:
        joystick = None

    try:
        throttle = hid.device()
        throttle.open(VENDOR_ID, THROTTLE_ID)
        throttle.set_nonblocking(True)
        print("Throttle opened")
    except:
        throttle = None

    print("Reading... Press Ctrl+C to stop")
    try:
        while True:
            if joystick:
                data = joystick.read(64)
                if data:
                    # Parse as 16-bit integers (skip first byte report ID)
                    # Pad with 0 if needed
                    payload = bytes(data[1:])
                    count = len(payload) // 2
                    ints = struct.unpack(f'<{count}H', payload[:count*2])
                    print(f"JOY: {ints}")
            
            if throttle:
                data = throttle.read(64)
                if data:
                    payload = bytes(data[1:])
                    count = len(payload) // 2
                    ints = struct.unpack(f'<{count}H', payload[:count*2])
                    print(f"THR: {ints}")
            
            time.sleep(0.05)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
