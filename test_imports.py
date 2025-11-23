#!/usr/bin/env python3
"""
Test all imports to identify missing dependencies
"""
import sys

def test_import(module_name, error_msg=None):
    try:
        __import__(module_name)
        print(f"✓ {module_name}")
        return True
    except ImportError as e:
        print(f"✗ {module_name}: {error_msg or str(e)}")
        return False

print("Testing CloudPad Dependencies...")
print("="*60)

# Core dependencies
all_ok = True
all_ok &= test_import('hid', 'hidapi')
all_ok &= test_import('websockets')
all_ok &= test_import('requests')
all_ok &= test_import('PIL', 'Pillow')

# PyQt6 (required)
print("\nPyQt6 modules:")
all_ok &= test_import('PyQt6.QtWidgets')
all_ok &= test_import('PyQt6.QtCore')
all_ok &= test_import('PyQt6.QtGui')

# Project modules
print("\nProject modules:")
all_ok &= test_import('device_manager')
all_ok &= test_import('universal_reader')
all_ok &= test_import('input_processor')
all_ok &= test_import('browser_bridge')
all_ok &= test_import('dsu_server')
all_ok &= test_import('license_validator')
all_ok &= test_import('build_config')

# UI modules
print("\nUI modules:")
all_ok &= test_import('ui.theme')
all_ok &= test_import('ui.main_window')
all_ok &= test_import('ui.calibration_dialog')
all_ok &= test_import('ui.calibration_logic')
all_ok &= test_import('ui.test_dialog')
all_ok &= test_import('ui.input_config_dialog')
all_ok &= test_import('ui.controller_visualizer')
all_ok &= test_import('ui.curve_editor')

print("="*60)
if all_ok:
    print("✓ All imports successful!")
    sys.exit(0)
else:
    print("✗ Some imports failed. Install missing dependencies.")
    sys.exit(1)
