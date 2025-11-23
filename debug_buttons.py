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
        print("Joystick opened. Press buttons or move Hat Switch...")
    except:
        print("Could not open Joystick.")
        return

    last_data = None

    print("Press Ctrl+C to stop.")
    try:
        while True:
            data = joystick.read(64)
            if data:
                # Convert to hex string for easy reading
                hex_str = " ".join(f"{b:02x}" for b in data)
                if data != last_data:
                    print(f"Data: {hex_str}")
                    last_data = data
            
            time.sleep(0.01)
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
