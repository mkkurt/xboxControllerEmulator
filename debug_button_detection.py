#!/usr/bin/env python3
"""
Interactive Button Detection Debugger
Let's see what's REALLY happening when you press buttons!
"""
import hid
import time
import sys

def debug_button_detection():
    print("="*70)
    print("INTERACTIVE BUTTON DETECTION DEBUGGER")
    print("="*70)

    # Find and open device
    print("\n1. Finding controllers...")
    devices = []
    for device_dict in hid.enumerate():
        usage_page = device_dict.get('usage_page', 0)
        usage = device_dict.get('usage', 0)
        if usage_page == 1 and usage in [4, 5, 8]:
            devices.append(device_dict)
            print(f"   Found: {device_dict.get('product_string')}")

    if not devices:
        print("✗ No controllers found!")
        return False

    # Use first device
    device_dict = devices[0]
    print(f"\n2. Using: {device_dict.get('product_string')}")

    try:
        dev = hid.device()
        dev.open(device_dict['vendor_id'], device_dict['product_id'])
        dev.set_nonblocking(True)
        print("   ✓ Device opened")
    except Exception as e:
        print(f"   ✗ Failed to open: {e}")
        return False

    print("\n" + "="*70)
    print("STEP 1: CAPTURE BASELINE")
    print("="*70)
    print("Don't press anything! Capturing baseline in 3 seconds...")

    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)

    # Capture baseline
    baseline = None
    for _ in range(10):
        data = dev.read(64, timeout_ms=100)
        if data:
            baseline = bytes(data)
            break
        time.sleep(0.05)

    if not baseline:
        print("✗ No data received!")
        return False

    print("\n✓ Baseline captured:")
    print("   First 16 bytes:", ' '.join(f'{b:02x}' for b in baseline[:16]))
    print("   All bytes:     ", ' '.join(f'{b:02x}' for b in baseline))

    print("\n" + "="*70)
    print("STEP 2: DETECT BUTTON PRESSES")
    print("="*70)
    print("\nNow I'll show you what changes when you press buttons.")
    print("Press buttons ONE AT A TIME and watch what happens!\n")
    print("Press Ctrl+C to stop.\n")

    last_report_time = 0

    try:
        while True:
            data = dev.read(64, timeout_ms=10)
            if not data:
                time.sleep(0.01)
                continue

            current = bytes(data)

            # Find all changes
            changes = []
            for i, (base, curr) in enumerate(zip(baseline, current)):
                diff = abs(int(curr) - int(base))
                if diff > 0:
                    changes.append((i, base, curr, diff))

            # Report changes (throttled to avoid spam)
            current_time = time.time()
            if changes and (current_time - last_report_time > 0.3):
                last_report_time = current_time

                print("-" * 70)
                print(f"DETECTED {len(changes)} CHANGE(S):")

                for byte_idx, base_val, curr_val, diff in changes[:10]:  # Show max 10
                    print(f"  Byte {byte_idx:2d}: {base_val:02x} → {curr_val:02x} (diff={diff:3d})")

                if len(changes) > 10:
                    print(f"  ... and {len(changes) - 10} more changes")

                # Show if it would be detected as button
                if len(changes) == 1:
                    byte_idx, base_val, curr_val, diff = changes[0]
                    print(f"\n  ✓ SINGLE CHANGE DETECTED!")
                    print(f"  → This would map to: Byte {byte_idx} = {curr_val:02x}")
                else:
                    print(f"\n  ✗ Multiple changes ({len(changes)}) - not a clean button press")
                    print(f"  → Probably axis movement or multiple buttons")

                print("-" * 70)
                print()

            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n\nStopped by user.")

    dev.close()

    print("\n" + "="*70)
    print("ANALYSIS & NEXT STEPS")
    print("="*70)
    print("""
What to look for:

1. SINGLE CHANGE when pressing ONE button:
   ✓ Good! Button detection should work.
   → Note the byte index and value.

2. MULTIPLE CHANGES when pressing ONE button:
   ✗ Problem! Could be:
      - Axes moving (don't touch sticks!)
      - Multiple bytes for one button (bitmask spread)
      - Noise in the HID data

3. NO CHANGES when pressing button:
   ✗ Problem! Could be:
      - Button already pressed in baseline
      - Button not working
      - Wrong device selected

NEXT: Tell me what you see when you press buttons!
      - How many changes?
      - Which byte indices?
      - What are the values?
    """)

    return True

if __name__ == "__main__":
    try:
        debug_button_detection()
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
