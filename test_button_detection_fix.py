#!/usr/bin/env python3
"""
Test the improved button detection logic against real button_debug.json data
"""
import json
from ui.calibration_logic import CalibrationLogic

def test_detection_logic():
    """Test the new detection logic with real data from button_debug.json"""

    # Load the debug data
    try:
        with open('button_debug.json', 'r') as f:
            debug_data = json.load(f)
    except FileNotFoundError:
        print("⚠ button_debug.json not found. Run auto_debug_buttons.py first.")
        return

    baseline = bytes(debug_data['baseline'])
    button_presses = debug_data['button_presses']

    print("=" * 70)
    print("BUTTON DETECTION FIX TEST")
    print("=" * 70)
    print(f"\nBaseline: {' '.join(f'{b:02x}' for b in baseline[:32])}")
    print(f"\nTesting {len(button_presses)} button press detections...\n")

    # Initialize logic
    logic = CalibrationLogic()
    logic.baseline_data = baseline

    # Simulate axes_config (empty since we're focusing on buttons)
    axes_config = {}

    # Track results
    old_logic_success = 0
    new_logic_success = 0

    for press in button_presses:
        detection_num = press['detection_num']
        changes = press['changes']

        # Reconstruct the raw data from changes
        raw_data = bytearray(baseline)
        for change in changes:
            raw_data[change['byte']] = change['current']

        # Test with new logic
        result = logic.detect_button(bytes(raw_data), axes_config)

        # Old logic would only detect single changes
        old_would_detect = press['is_single_change']
        new_detected = result is not None

        if old_would_detect:
            old_logic_success += 1
        if new_detected:
            new_logic_success += 1

        # Show results
        status = "✓" if new_detected else "✗"
        print(f"[{detection_num:2d}] {status} Changes: {len(changes)}", end="")

        if len(changes) <= 3:
            change_str = ', '.join(f"byte {c['byte']}={c['current']:02x}(Δ{c['diff']})" for c in changes)
            print(f" - {change_str}")
        else:
            change_str = ', '.join(f"byte {c['byte']}={c['current']:02x}(Δ{c['diff']})" for c in changes[:3])
            print(f" - {change_str}, ... +{len(changes)-3} more")

        if new_detected:
            byte_idx, value = result
            print(f"     → Detected: Byte {byte_idx} = {value:02x}", end="")
            if hasattr(logic, 'last_filter_reason'):
                print(f" ({logic.last_filter_reason})")
            else:
                print(" (single change)")

        if old_would_detect != new_detected:
            if new_detected:
                print(f"     ✓ NEW LOGIC FIXED THIS! (old logic missed it)")
            else:
                print(f"     ⚠ New logic missed this (old logic would too)")

    print("\n" + "=" * 70)
    print("RESULTS SUMMARY")
    print("=" * 70)
    print(f"Total button presses tested: {len(button_presses)}")
    print(f"Old logic success: {old_logic_success}/{len(button_presses)} ({old_logic_success/len(button_presses)*100:.1f}%)")
    print(f"New logic success: {new_logic_success}/{len(button_presses)} ({new_logic_success/len(button_presses)*100:.1f}%)")
    print(f"\nImprovement: {new_logic_success - old_logic_success} additional detections")
    print(f"Success rate improved by: {(new_logic_success - old_logic_success)/len(button_presses)*100:.1f}%")

    if new_logic_success >= len(button_presses) * 0.8:  # 80% or better
        print("\n✓ EXCELLENT! New logic achieves ≥80% success rate.")
    elif new_logic_success > old_logic_success:
        print(f"\n✓ IMPROVED! New logic is better than old ({new_logic_success} vs {old_logic_success})")
    else:
        print("\n⚠ No improvement. Need to adjust thresholds.")

    print("=" * 70)

if __name__ == "__main__":
    test_detection_logic()
