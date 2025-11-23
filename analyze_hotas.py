import hid
import time

# HOTAS Warthog IDs
VENDOR_ID = 0x044f
JOYSTICK_ID = 0x0402
THROTTLE_ID = 0x0404

def print_hex(data):
    return " ".join(f"{b:02x}" for b in data)

def main():
    print("Opening HOTAS Warthog devices...")
    
    joystick = None
    throttle = None

    try:
        joystick = hid.device()
        joystick.open(VENDOR_ID, JOYSTICK_ID)
        print(f"Joystick opened: {joystick.get_manufacturer_string()} {joystick.get_product_string()}")
        joystick.set_nonblocking(True)
    except Exception as e:
        print(f"Could not open Joystick: {e}")

    try:
        throttle = hid.device()
        throttle.open(VENDOR_ID, THROTTLE_ID)
        print(f"Throttle opened: {throttle.get_manufacturer_string()} {throttle.get_product_string()}")
        throttle.set_nonblocking(True)
    except Exception as e:
        print(f"Could not open Throttle: {e}")

    if not joystick and not throttle:
        print("No devices found. Exiting.")
        return

    print("\nListening for input... (Press Ctrl+C to stop)")
    print("Try moving the stick/throttle and pressing buttons to see the data changes.")

    try:
        while True:
            if joystick:
                data = joystick.read(64)
                if data:
                    print(f"JOYSTICK: {print_hex(data)}")
            
            if throttle:
                data = throttle.read(64)
                if data:
                    print(f"THROTTLE: {print_hex(data)}")
            
            time.sleep(0.01)
            
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        if joystick: joystick.close()
        if throttle: throttle.close()

if __name__ == "__main__":
    main()
