#!/usr/bin/env python3
"""
Automated Test Suite for CloudPad
Tests all core functionality
"""
import sys
import time
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.append(str(Path(__file__).parent.parent))

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def test(self, name, func):
        """Run a test function"""
        print(f"\n{'='*60}")
        print(f"TEST: {name}")
        print('='*60)
        try:
            result = func()
            if result:
                print(f"✓ PASS: {name}")
                self.passed += 1
            else:
                print(f"✗ FAIL: {name}")
                self.failed += 1
        except Exception as e:
            print(f"✗ ERROR: {name}")
            print(f"  {type(e).__name__}: {e}")
            self.failed += 1
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print("TEST SUMMARY")
        print('='*60)
        print(f"Total: {total}")
        print(f"Passed: {self.passed} ({self.passed/total*100:.0f}%)")
        print(f"Failed: {self.failed}")
        return self.failed == 0

def test_device_detection():
    """Test device manager can detect controllers"""
    from device_manager import DeviceManager
    dm = DeviceManager()
    devices = dm.scan_devices()
    print(f"  Found {len(devices)} device(s)")
    for d in devices:
        print(f"    - {d}")
    return len(devices) > 0

def test_license_validation():
    """Test license system"""
    from license_validator import LicenseValidator
    lv = LicenseValidator()
    
    # Test key format validation
    valid_key = "AA56-70D9-986E-77E9"
    invalid_key = "INVALID-KEY"
    
    result1 = lv.validate_license_key(valid_key)
    result2 = not lv.validate_license_key(invalid_key)
    
    print(f"  Valid key check: {'✓' if result1 else '✗'}")
    print(f"  Invalid key rejection: {'✓' if result2 else '✗'}")
    
    # Test tier features
    features = lv.get_tier_features()
    print(f"  Features: {features}")
    
    return result1 and result2 and features

def test_universal_reader():
    """Test universal input reader"""
    from universal_reader import UniversalInputReader
    reader = UniversalInputReader()
    
    started = reader.start()
    print(f"  Reader started: {'✓' if started else '✗'}")
    
    if started:
        time.sleep(0.5)
        state = reader.get_state()
        print(f"  State keys: {len(state)}")
        reader.stop()
        return True
    return False

def test_browser_bridge():
    """Test WebSocket server"""
    from browser_bridge import BrowserBridge
    bridge = BrowserBridge(port=8766)  # Different port to avoid conflicts
    
    bridge.start()
    print("  Server started")
    
    time.sleep(1)
    
    # Test broadcast
    test_state = {'test': 123}
    bridge.broadcast(test_state)
    print("  Broadcast test completed")
    
    bridge.stop()
    print("  Server stopped")
    
    return True

def test_auto_calibrate():
    """Test calibration wizard exists and is executable"""
    cal_file = Path("ui/calibration_dialog.py")
    exists = cal_file.exists()
    print(f"  File exists: {'✓' if exists else '✗'}")
    
    if exists:
        with open(cal_file) as f:
            content = f.read()
            has_wizard = "CalibrationDialog" in content
            print(f"  Has CalibrationDialog class: {'✓' if has_wizard else '✗'}")
            return has_wizard
    return False

def test_gui_imports():
    """Test GUI can be imported"""
    try:
        from ui.main_window import CloudPadWindow
        print("  CloudPadWindow imported successfully")
        return True
    except Exception as e:
        print(f"  Import failed: {e}")
        return False

def test_extension_files():
    """Test browser extension files exist"""
    ext_path = Path("extension")
    required_files = [
        "manifest.json",
        "content.js",
        "background.js",
        "popup.html",
        "popup.js"
    ]
    
    all_exist = True
    for file in required_files:
        exists = (ext_path / file).exists()
        print(f"  {file}: {'✓' if exists else '✗'}")
        all_exist = all_exist and exists
    
    return all_exist

def main():
    runner = TestRunner()
    
    print("CloudPad Automated Test Suite")
    print("Testing all core components...\n")
    
    runner.test("Device Detection", test_device_detection)
    runner.test("License Validation", test_license_validation)
    runner.test("Universal Input Reader", test_universal_reader)
    runner.test("Browser Bridge", test_browser_bridge)
    runner.test("Auto-Calibration", test_auto_calibrate)
    runner.test("GUI Imports", test_gui_imports)
    runner.test("Browser Extension Files", test_extension_files)
    
    success = runner.summary()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
