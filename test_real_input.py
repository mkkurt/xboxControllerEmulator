#!/usr/bin/env python3
"""
Test REAL input reading from actual connected HOTAS controllers
This will read actual HID data and verify the input system works
"""
from universal_reader import UniversalInputReader
from device_manager import DeviceManager
import time
import sys

def test_real_input():
    print("="*60)
    print("REAL HARDWARE INPUT TEST")
    print("="*60)

    # Initialize
    print("\n1. Initializing device manager...")
    device_manager = DeviceManager()

    # Scan for devices
    print("\n2. Scanning for connected controllers...")
    devices = device_manager.scan_devices()

    if not devices:
        print("✗ NO CONTROLLERS DETECTED!")
        print("Please connect a controller and try again.")
        return False

    print(f"✓ Found {len(devices)} controller(s):")
    for i, dev in enumerate(devices):
        config = device_manager.get_device_config(dev)
        status = "CONFIGURED" if config else "NOT CONFIGURED"
        print(f"  {i+1}. {dev} - {status}")

    # Initialize reader
    print("\n3. Starting universal input reader...")
    reader = UniversalInputReader(device_manager)

    if not reader.start():
        print("✗ FAILED to start reader!")
        print("This might mean no configured devices exist.")
        print("Run calibration first if needed.")
        return False

    print("✓ Input reader started successfully")
    print(f"  Active devices: {len(reader.active_devices)}")

    # Read input for 5 seconds
    print("\n4. Reading input for 5 seconds...")
    print("   >>> MOVE YOUR CONTROLLER NOW <<<")
    print("   (Press buttons, move sticks, etc.)\n")

    start_time = time.time()
    last_state = {}
    changes_detected = 0

    try:
        while time.time() - start_time < 5:
            state = reader.get_state()

            # Check for changes
            for key, value in state.items():
                if key not in last_state or last_state[key] != value:
                    changes_detected += 1
                    # Print significant changes
                    if isinstance(value, bool) and value:
                        print(f"  ✓ Button: {key} = {value}")
                    elif isinstance(value, (int, float)) and abs(value) > 0.1:
                        print(f"  ✓ Axis: {key} = {value:.3f}")

            last_state = state.copy()
            time.sleep(0.05)  # 20 Hz

    except KeyboardInterrupt:
        print("\n  Interrupted by user")

    reader.stop()

    print("\n" + "="*60)
    print("TEST RESULTS:")
    print(f"  Input changes detected: {changes_detected}")

    if changes_detected > 0:
        print("  ✓ CONTROLLER INPUT WORKING!")
        print("  ✓ Hardware communication successful")
        return True
    else:
        print("  ⚠ No input detected")
        print("  Possible reasons:")
        print("    - Controller not configured (run calibration)")
        print("    - Controller not moved during test")
        print("    - Device permissions issue")
        return False

if __name__ == "__main__":
    success = test_real_input()
    sys.exit(0 if success else 1)
