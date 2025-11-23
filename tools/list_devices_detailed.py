import hid

print("Listing HID devices with details...")
try:
    for device in hid.enumerate():
        print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")
        print(f"  Usage Page: {device.get('usage_page')}")
        print(f"  Usage: {device.get('usage')}")
        print(f"  Path: {device.get('path')}")
        print("-" * 40)
except Exception as e:
    print(f"Error enumerating devices: {e}")
