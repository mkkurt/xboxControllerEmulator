#!/usr/bin/env python3
"""
Automated Button Detection Debugger
Runs for 15 seconds, saves everything to file
"""
import hid
import time
import json

def auto_debug():
    output = {
        'baseline': None,
        'button_presses': [],
        'summary': {}
    }

    # Find device
    devices = []
    for device_dict in hid.enumerate():
        usage_page = device_dict.get('usage_page', 0)
        usage = device_dict.get('usage', 0)
        if usage_page == 1 and usage in [4, 5, 8]:
            devices.append(device_dict)

    if not devices:
        output['error'] = "No controllers found"
        with open('button_debug.json', 'w') as f:
            json.dump(output, f, indent=2)
        return

    device_dict = devices[0]
    output['device'] = device_dict.get('product_string')

    try:
        dev = hid.device()
        dev.open(device_dict['vendor_id'], device_dict['product_id'])
        dev.set_nonblocking(True)
    except Exception as e:
        output['error'] = str(e)
        with open('button_debug.json', 'w') as f:
            json.dump(output, f, indent=2)
        return

    print("Waiting 2 seconds for baseline (don't press anything)...")
    time.sleep(2)

    # Capture baseline
    baseline = None
    for _ in range(20):
        data = dev.read(64, timeout_ms=100)
        if data:
            baseline = bytes(data)
            break
        time.sleep(0.05)

    if not baseline:
        output['error'] = "No data received"
        with open('button_debug.json', 'w') as f:
            json.dump(output, f, indent=2)
        return

    output['baseline'] = list(baseline)

    print(f"✓ Baseline captured: {' '.join(f'{b:02x}' for b in baseline[:16])}...")
    print("\nNow monitoring for 15 seconds...")
    print(">>> PRESS BUTTONS ONE AT A TIME <<<")
    print("I'll record everything automatically.\n")

    start_time = time.time()
    last_detection = 0
    detection_count = 0

    while time.time() - start_time < 15:
        data = dev.read(64, timeout_ms=10)
        if not data:
            time.sleep(0.01)
            continue

        current = bytes(data)
        current_time = time.time()

        # Find changes
        changes = []
        for i, (base, curr) in enumerate(zip(baseline, current)):
            diff = abs(int(curr) - int(base))
            if diff > 0:
                changes.append({
                    'byte': i,
                    'baseline': base,
                    'current': curr,
                    'diff': diff
                })

        # Record if changes detected and enough time passed
        if changes and (current_time - last_detection > 0.5):
            last_detection = current_time
            detection_count += 1

            press_data = {
                'detection_num': detection_count,
                'timestamp': current_time - start_time,
                'num_changes': len(changes),
                'changes': changes,
                'is_single_change': len(changes) == 1
            }

            output['button_presses'].append(press_data)

            print(f"[{detection_count}] Detected {len(changes)} change(s)")
            if len(changes) == 1:
                ch = changes[0]
                print(f"    ✓ Byte {ch['byte']}: {ch['baseline']:02x} → {ch['current']:02x}")
            else:
                for ch in changes[:3]:
                    print(f"    • Byte {ch['byte']}: {ch['baseline']:02x} → {ch['current']:02x}")
                if len(changes) > 3:
                    print(f"    ... and {len(changes)-3} more")

        time.sleep(0.01)

    dev.close()

    # Summary
    single_changes = [p for p in output['button_presses'] if p['is_single_change']]
    multi_changes = [p for p in output['button_presses'] if not p['is_single_change']]

    output['summary'] = {
        'total_detections': len(output['button_presses']),
        'single_change_detections': len(single_changes),
        'multi_change_detections': len(multi_changes),
        'success_rate': f"{len(single_changes)}/{len(output['button_presses'])}"
    }

    # Analyze which bytes are most common in single changes
    if single_changes:
        byte_freq = {}
        for press in single_changes:
            byte_idx = press['changes'][0]['byte']
            if byte_idx not in byte_freq:
                byte_freq[byte_idx] = []
            byte_freq[byte_idx].append(press['changes'][0]['current'])
        output['summary']['button_bytes'] = byte_freq

    # Save to file
    with open('button_debug.json', 'w') as f:
        json.dump(output, f, indent=2)

    print("\n" + "="*60)
    print("DONE! Results saved to button_debug.json")
    print("="*60)
    print(f"Total detections: {len(output['button_presses'])}")
    print(f"Single changes: {len(single_changes)} ✓")
    print(f"Multiple changes: {len(multi_changes)} ✗")

    if single_changes:
        print("\nButtons detected (single change):")
        for byte_idx, values in byte_freq.items():
            print(f"  Byte {byte_idx}: values = {set(values)}")

if __name__ == "__main__":
    auto_debug()
