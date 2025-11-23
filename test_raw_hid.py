#!/usr/bin/env python3
"""
Test RAW HID data reading from controllers
This bypasses all configuration and just reads raw bytes
"""
import hid
import time

def test_raw_hid():
    print("="*60)
    print("RAW HID DATA TEST")
    print("="*60)

    # Find all HID devices
    print("\n1. Enumerating HID devices...")
    devices = []
    for device_dict in hid.enumerate():
        usage_page = device_dict.get('usage_page', 0)
        usage = device_dict.get('usage', 0)

        # Controller devices
        if usage_page == 1 and usage in [4, 5, 8]:
            devices.append(device_dict)
            print(f"  Found: {device_dict.get('manufacturer_string')} {device_dict.get('product_string')}")
            print(f"    VID:PID: {device_dict['vendor_id']:04x}:{device_dict['product_id']:04x}")
            print(f"    Usage: {usage}")

    if not devices:
        print("✗ No HID controllers found!")
        return False

    # Try to open and read from first device
    print(f"\n2. Testing first device...")
    device_dict = devices[0]

    try:
        dev = hid.device()
        dev.open(device_dict['vendor_id'], device_dict['product_id'])
        dev.set_nonblocking(True)
        print(f"  ✓ Opened: {device_dict.get('product_string')}")
    except Exception as e:
        print(f"  ✗ Failed to open: {e}")
        return False

    # Read raw data
    print("\n3. Reading raw HID data for 3 seconds...")
    print("   >>> MOVE THE CONTROLLER NOW <<<\n")

    start_time = time.time()
    data_count = 0
    last_data = None

    while time.time() - start_time < 3:
        try:
            data = dev.read(64, timeout_ms=10)
            if data:
                data_count += 1
                # Only print if data changed
                if data != last_data:
                    hex_str = ' '.join(f'{b:02x}' for b in data[:16])
                    print(f"  Data: [{hex_str}...]")
                    last_data = data
        except Exception as e:
            print(f"  Error reading: {e}")
            break

        time.sleep(0.01)

    dev.close()

    print("\n" + "="*60)
    print("TEST RESULTS:")
    print(f"  Data packets received: {data_count}")

    if data_count > 0:
        print("  ✓ RAW HID COMMUNICATION WORKING!")
        print("  ✓ Controller is sending data")
        return True
    else:
        print("  ✗ No data received")
        print("  Possible issues:")
        print("    - Permissions problem")
        print("    - Controller not connected properly")
        print("    - Driver issue")
        return False

if __name__ == "__main__":
    import sys
    success = test_raw_hid()
    sys.exit(0 if success else 1)
