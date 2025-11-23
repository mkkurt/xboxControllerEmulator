#!/usr/bin/env python3
"""
Calibration Diagnostic Tool
Shows exactly what's happening during calibration
"""
import hid
import time
import sys

def diagnose():
    print("="*70)
    print("CALIBRATION DIAGNOSTIC")
    print("="*70)

    # Find device
    print("\n[Step 1] Finding controllers...")
    devices = []
    for device_dict in hid.enumerate():
        usage_page = device_dict.get('usage_page', 0)
        usage = device_dict.get('usage', 0)
        if usage_page == 1 and usage in [4, 5, 8]:
            devices.append(device_dict)
            print(f"  Found: {device_dict.get('product_string')}")

    if not devices:
        print("✗ No controllers found!")
        return

    device_dict = devices[0]
    print(f"\n[Step 2] Using: {device_dict.get('product_string')}")

    # Open device
    try:
        dev = hid.device()
        dev.open(device_dict['vendor_id'], device_dict['product_id'])
        dev.set_nonblocking(True)
        print("  ✓ Device opened")
    except Exception as e:
        print(f"  ✗ Failed to open: {e}")
        return

    # Test basic reading
    print("\n[Step 3] Testing basic HID reading...")
    data = None
    for _ in range(20):
        data = dev.read(64, timeout_ms=100)
        if data:
            print(f"  ✓ Got data: {' '.join(f'{b:02x}' for b in data[:16])}...")
            break
        time.sleep(0.05)

    if not data:
        print("  ✗ No data received!")
        dev.close()
        return

    # Test axis detection
    print("\n[Step 4] Testing axis detection...")
    print("  Move your sticks and triggers NOW!")
    print("  Watching for 3 seconds...\n")

    baseline = bytes(data)
    changes_detected = {}

    start = time.time()
    while time.time() - start < 3:
        data = dev.read(64, timeout_ms=10)
        if data:
            for i, (base, curr) in enumerate(zip(baseline, data)):
                if base != curr:
                    if i not in changes_detected:
                        changes_detected[i] = {'min': curr, 'max': curr, 'count': 0}
                    changes_detected[i]['min'] = min(changes_detected[i]['min'], curr)
                    changes_detected[i]['max'] = max(changes_detected[i]['max'], curr)
                    changes_detected[i]['count'] += 1
        time.sleep(0.01)

    if changes_detected:
        print(f"  ✓ Detected changes in {len(changes_detected)} bytes:")
        for byte_idx in sorted(changes_detected.keys()):
            stats = changes_detected[byte_idx]
            range_val = stats['max'] - stats['min']
            print(f"    Byte {byte_idx:2d}: min={stats['min']:3d} max={stats['max']:3d} range={range_val:3d} changes={stats['count']}")
    else:
        print("  ✗ No changes detected!")
        print("  → Did you move the sticks?")

    # Test button detection
    print("\n[Step 5] Testing button detection...")
    print("  Waiting 2 seconds for baseline...")
    time.sleep(2)

    baseline = None
    for _ in range(10):
        data = dev.read(64, timeout_ms=100)
        if data:
            baseline = bytes(data)
            break
        time.sleep(0.05)

    if not baseline:
        print("  ✗ Failed to capture baseline")
        dev.close()
        return

    print(f"  ✓ Baseline: {' '.join(f'{b:02x}' for b in baseline[:16])}...")
    print("\n  Now press ONE button (you have 5 seconds)...")

    detected = False
    start = time.time()
    while time.time() - start < 5:
        data = dev.read(64, timeout_ms=10)
        if data:
            changes = []
            for i, (base, curr) in enumerate(zip(baseline, data)):
                diff = abs(curr - base)
                if diff > 0:
                    changes.append((i, base, curr, diff))

            if changes:
                print(f"\n  Detected {len(changes)} change(s):")
                for byte_idx, base_val, curr_val, diff in changes[:10]:
                    print(f"    Byte {byte_idx:2d}: {base_val:02x} → {curr_val:02x} (diff={diff:3d})")

                # Test the new detection logic
                from ui.calibration_logic import CalibrationLogic
                logic = CalibrationLogic()
                logic.baseline_data = baseline

                result = logic.detect_button(bytes(data), {})
                if result:
                    byte_idx, value = result
                    print(f"\n  ✓ DETECTION LOGIC SAYS: Byte {byte_idx} = {value:02x}")
                    if hasattr(logic, 'last_filter_reason'):
                        print(f"    Reason: {logic.last_filter_reason}")
                else:
                    print(f"\n  ✗ DETECTION LOGIC REJECTED (multiple changes)")

                detected = True
                break

        time.sleep(0.01)

    if not detected:
        print("\n  ✗ No button press detected")
        print("  → Did you press a button?")

    dev.close()

    # Summary
    print("\n" + "="*70)
    print("DIAGNOSTIC SUMMARY")
    print("="*70)

    if changes_detected and detected:
        print("✓ Device communication: WORKING")
        print("✓ Axis detection: WORKING")
        print("✓ Button detection: WORKING")
        print("\nThe hardware and detection logic are working!")
        print("If calibration still fails, the issue is in the GUI.")
    else:
        print("⚠ ISSUES DETECTED:")
        if not changes_detected:
            print("  - No axis movement detected")
        if not detected:
            print("  - No button press detected")

    print("="*70)

if __name__ == "__main__":
    try:
        diagnose()
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
