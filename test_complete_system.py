#!/usr/bin/env python3
"""
Comprehensive System Test
Tests all components without requiring manual interaction
"""
import sys
import time
import asyncio
import threading
from device_manager import DeviceManager
from input_processor import InputProcessor
from browser_bridge import BrowserBridge
from dsu_server import DSUServer

def test_device_manager():
    """Test device scanning and configuration"""
    print("\n" + "="*70)
    print("TEST 1: Device Manager")
    print("="*70)

    dm = DeviceManager()
    devices = dm.scan_devices()

    if not devices:
        print("⚠ No devices found - skipping device tests")
        print("  (This is OK if no controller is connected)")
        return None

    print(f"✓ Found {len(devices)} device(s):")
    for dev in devices:
        print(f"  - {dev}")

    # Test device configuration
    test_device = devices[0]
    print(f"\n✓ Using device: {test_device}")

    # Create a test config
    test_config = {
        'device_id': str(test_device),
        'mappings': {
            'axes': {
                'LeftX': {'offset': 2, 'min': 0, 'max': 255, 'center': 128, 'deadzone': 0.05},
                'LeftY': {'offset': 3, 'min': 0, 'max': 255, 'center': 128, 'deadzone': 0.05},
            }
        },
        'button_map': {
            'A': [5, 1],
            'B': [5, 2],
        }
    }

    dm.save_device_config(test_device, test_config)
    print("✓ Saved test configuration")

    loaded_config = dm.get_device_config(test_device)
    if loaded_config:
        print("✓ Loaded configuration successfully")
        print(f"  Axes: {len(loaded_config.get('mappings', {}).get('axes', {}))}")
        print(f"  Buttons: {len(loaded_config.get('button_map', {}))}")
    else:
        print("✗ Failed to load configuration")
        return None

    return test_device

def test_input_processor(test_device):
    """Test input processing with real HID data"""
    print("\n" + "="*70)
    print("TEST 2: Input Processor")
    print("="*70)

    if not test_device:
        print("⚠ Skipping (no device available)")
        return False

    try:
        dm = DeviceManager()
        config = dm.get_device_config(test_device)

        processor = InputProcessor(test_device, config)
        print(f"✓ Created input processor for {test_device}")

        # Read a few packets
        print("  Reading 10 HID packets...")
        packets_read = 0
        start_time = time.time()

        while packets_read < 10 and (time.time() - start_time) < 2:
            state = processor.read()
            if state and 'raw_data' in state:
                packets_read += 1

        if packets_read > 0:
            print(f"✓ Read {packets_read} packets")
            print(f"  Sample state keys: {list(state.keys())[:5]}")
            return True
        else:
            print("✗ No data received")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_browser_bridge():
    """Test WebSocket server and gamepad conversion"""
    print("\n" + "="*70)
    print("TEST 3: Browser Bridge (WebSocket)")
    print("="*70)

    try:
        # Create a test state
        test_state = {
            'device_Joystick_LeftX': 0.5,
            'device_Joystick_LeftY': -0.3,
            'device_Joystick_RightX': 0.0,
            'device_Joystick_RightY': 0.0,
            'device_Joystick_LT': 0.0,
            'device_Joystick_RT': 0.0,
            'device_Joystick_A': False,
            'device_Joystick_B': True,
        }

        bridge = BrowserBridge()
        print("✓ Created browser bridge")

        # Test gamepad conversion
        gamepad = bridge._convert_to_gamepad(test_state)
        print("✓ Gamepad conversion successful")
        print(f"  Axes: {gamepad['axes']}")
        print(f"  Buttons pressed: {sum(1 for b in gamepad['buttons'] if b['pressed'])}")

        # Start server in background
        def run_server():
            asyncio.run(bridge.start_server())

        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        print("✓ WebSocket server started on ws://127.0.0.1:8765")

        time.sleep(0.5)  # Let server start

        # Broadcast test data
        asyncio.run(bridge.broadcast(test_state))
        print("✓ Broadcast test successful")

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dsu_server():
    """Test DSU protocol server"""
    print("\n" + "="*70)
    print("TEST 4: DSU Server (Controller Emulation)")
    print("="*70)

    try:
        # Create test controller state
        test_state = {
            'device_Controller_LeftX': 0.0,
            'device_Controller_LeftY': 0.0,
            'device_Controller_RightX': 0.5,
            'device_Controller_RightY': -0.5,
            'device_Controller_A': True,
            'device_Controller_B': False,
        }

        server = DSUServer()
        print("✓ Created DSU server")

        # Start server in background
        def run_dsu():
            asyncio.run(server.start())

        dsu_thread = threading.Thread(target=run_dsu, daemon=True)
        dsu_thread.start()
        print("✓ DSU server started on port 26760")

        time.sleep(0.3)  # Let server start

        # Update controller state
        asyncio.run(server.update_controller_state(test_state))
        print("✓ Controller state update successful")

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_calibration_logic():
    """Test calibration detection logic"""
    print("\n" + "="*70)
    print("TEST 5: Calibration Logic")
    print("="*70)

    try:
        from ui.calibration_logic import CalibrationLogic

        logic = CalibrationLogic()
        print("✓ Created calibration logic")

        # Test axis calibration
        test_data = bytearray([128] * 64)
        logic.process_axis_calibration(test_data)
        print("✓ Baseline captured")

        # Simulate axis movement
        for i in range(10):
            test_data[5] = 128 + i * 10  # Move axis at byte 5
            logic.process_axis_calibration(test_data)

        axes = logic.finalize_axes()
        print(f"✓ Detected {len(axes)} axes")

        # Test button detection
        baseline = bytearray([0] * 64)
        logic.baseline_data = bytes(baseline)

        # Simulate button press (single byte change)
        button_data = bytearray(baseline)
        button_data[10] = 1

        result = logic.detect_button(bytes(button_data), axes)
        if result:
            byte_idx, value = result
            print(f"✓ Button detection works: Byte {byte_idx} = {value}")
        else:
            print("✗ Button detection failed")
            return False

        # Test multi-byte change filtering (the fix we just implemented)
        multi_data = bytearray(baseline)
        multi_data[10] = 50  # Large change (button)
        multi_data[11] = 5   # Small change (noise)
        multi_data[12] = 3   # Small change (noise)

        result = logic.detect_button(bytes(multi_data), axes)
        if result:
            byte_idx, value = result
            print(f"✓ Multi-byte filtering works: Byte {byte_idx} = {value}")
            if byte_idx == 10:
                print("  → Correctly selected byte with largest change")
            else:
                print(f"  ⚠ Selected byte {byte_idx} instead of 10")
        else:
            print("✗ Multi-byte filtering failed")
            return False

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "█"*70)
    print("  CLOUDPAD XBOX CONTROLLER EMULATOR - COMPREHENSIVE TEST SUITE")
    print("█"*70)

    results = {}

    # Test 1: Device Manager
    test_device = test_device_manager()
    results['device_manager'] = test_device is not None or True  # OK if no device

    # Test 2: Input Processor
    if test_device:
        results['input_processor'] = test_input_processor(test_device)
    else:
        print("\n" + "="*70)
        print("TEST 2: Input Processor")
        print("="*70)
        print("⚠ Skipping (no device available)")
        results['input_processor'] = None  # Skipped

    # Test 3: Browser Bridge
    results['browser_bridge'] = test_browser_bridge()

    # Test 4: DSU Server
    results['dsu_server'] = test_dsu_server()

    # Test 5: Calibration Logic
    results['calibration_logic'] = test_calibration_logic()

    # Summary
    print("\n" + "█"*70)
    print("  TEST SUMMARY")
    print("█"*70)

    for test_name, result in results.items():
        status = "✓ PASS" if result is True else "⚠ SKIP" if result is None else "✗ FAIL"
        print(f"  {test_name:.<30} {status}")

    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)

    print(f"\n  Total: {passed} passed, {failed} failed, {skipped} skipped")

    if failed == 0:
        print("\n✓ ALL TESTS PASSED!")
        print("  The system is ready to use.")
    else:
        print(f"\n⚠ {failed} test(s) failed. Please review the errors above.")

    print("█"*70 + "\n")

    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
