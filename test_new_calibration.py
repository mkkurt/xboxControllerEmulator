#!/usr/bin/env python3
"""
Test the new calibration dialog
"""
import sys
from PyQt6.QtWidgets import QApplication
from device_manager import DeviceManager
from ui.calibration_dialog_new import SimpleCalibrationDialog

def main():
    print("="*70)
    print("Testing New Calibration Dialog")
    print("="*70)

    # Test imports
    print("\n[1/3] Testing imports...")
    try:
        from ui.calibration_logic import CalibrationLogic
        print("  ✓ CalibrationLogic imported")
        print("  ✓ SimpleCalibrationDialog imported")
        print("  ✓ All imports successful")
    except Exception as e:
        print(f"  ✗ Import error: {e}")
        return False

    # Test device manager
    print("\n[2/3] Testing device manager...")
    try:
        dm = DeviceManager()
        devices = dm.scan_devices()
        if devices:
            print(f"  ✓ Found {len(devices)} device(s)")
            for dev in devices:
                print(f"    - {dev}")
        else:
            print("  ⚠ No devices found (this is OK)")
    except Exception as e:
        print(f"  ✗ Device manager error: {e}")
        return False

    # Test dialog creation
    print("\n[3/3] Testing dialog creation...")
    try:
        app = QApplication(sys.argv)
        dialog = SimpleCalibrationDialog(dm)
        print("  ✓ Dialog created successfully")
        print("  ✓ Ready to show dialog")

        # Uncomment to actually show the dialog:
        # dialog.exec()

        print("\n" + "="*70)
        print("✓ All tests passed!")
        print("="*70)
        print("\nThe new calibration dialog is ready to use.")
        print("To test with GUI, run: python3 main.py")
        return True

    except Exception as e:
        print(f"  ✗ Dialog creation error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
