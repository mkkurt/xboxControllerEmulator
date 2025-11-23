#!/usr/bin/env python3
"""
Comprehensive Project Verification Script
Checks all files, imports, and structure
"""
import os
import sys
from pathlib import Path

def check_file(path, description):
    """Check if a file exists"""
    if os.path.exists(path):
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - MISSING!")
        return False

def check_directory(path, description):
    """Check if a directory exists"""
    if os.path.isdir(path):
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - MISSING!")
        return False

def main():
    print("CloudPad Project Verification")
    print("="*60)

    all_ok = True

    # Check core Python files
    print("\nCore Python Modules:")
    all_ok &= check_file("main.py", "main.py (Entry point)")
    all_ok &= check_file("device_manager.py", "device_manager.py")
    all_ok &= check_file("universal_reader.py", "universal_reader.py")
    all_ok &= check_file("input_processor.py", "input_processor.py")
    all_ok &= check_file("browser_bridge.py", "browser_bridge.py")
    all_ok &= check_file("dsu_server.py", "dsu_server.py")
    all_ok &= check_file("license_validator.py", "license_validator.py")
    all_ok &= check_file("build_config.py", "build_config.py")

    # Check UI directory and files
    print("\nUI Components:")
    all_ok &= check_directory("ui", "ui/ directory")
    all_ok &= check_file("ui/__init__.py", "ui/__init__.py")
    all_ok &= check_file("ui/main_window.py", "ui/main_window.py")
    all_ok &= check_file("ui/calibration_dialog.py", "ui/calibration_dialog.py")
    all_ok &= check_file("ui/calibration_logic.py", "ui/calibration_logic.py")
    all_ok &= check_file("ui/test_dialog.py", "ui/test_dialog.py")
    all_ok &= check_file("ui/input_config_dialog.py", "ui/input_config_dialog.py")
    all_ok &= check_file("ui/controller_visualizer.py", "ui/controller_visualizer.py")
    all_ok &= check_file("ui/curve_editor.py", "ui/curve_editor.py")
    all_ok &= check_file("ui/theme.py", "ui/theme.py")

    # Check extension directory
    print("\nBrowser Extension:")
    all_ok &= check_directory("extension", "extension/ directory")
    all_ok &= check_file("extension/manifest.json", "extension/manifest.json")
    all_ok &= check_file("extension/content.js", "extension/content.js")
    all_ok &= check_file("extension/background.js", "extension/background.js")
    all_ok &= check_file("extension/popup.html", "extension/popup.html")
    all_ok &= check_file("extension/popup.js", "extension/popup.js")
    all_ok &= check_file("extension/icon16.png", "extension/icon16.png")
    all_ok &= check_file("extension/icon48.png", "extension/icon48.png")
    all_ok &= check_file("extension/icon128.png", "extension/icon128.png")

    # Check presets directory
    print("\nDevice Presets:")
    all_ok &= check_directory("presets", "presets/ directory")
    preset_count = len(list(Path("presets").glob("*.json"))) if os.path.exists("presets") else 0
    print(f"  Found {preset_count} preset file(s)")

    # Check documentation
    print("\nDocumentation:")
    all_ok &= check_file("README.md", "README.md")
    all_ok &= check_file("requirements.txt", "requirements.txt")

    # Check configuration files
    print("\nConfiguration:")
    all_ok &= check_file("CloudPad.spec", "CloudPad.spec (PyInstaller)")

    # Check for common issues
    print("\nCommon Issues Check:")

    # Check for PyQt6 import
    try:
        import PyQt6
        print("✓ PyQt6 is installed")
    except ImportError:
        print("⚠ PyQt6 is NOT installed (required for GUI)")
        print("  Run: pip3 install PyQt6")

    # Check for hidapi
    try:
        import hid
        print("✓ hidapi is installed")
    except ImportError:
        print("✗ hidapi is NOT installed (required)")
        all_ok = False

    # Check for websockets
    try:
        import websockets
        print("✓ websockets is installed")
    except ImportError:
        print("✗ websockets is NOT installed (required)")
        all_ok = False

    # Summary
    print("\n" + "="*60)
    if all_ok:
        print("✓ Project structure is complete!")
        print("\nNote: PyQt6 is required for the GUI application.")
        print("Install it with: pip3 install PyQt6")
    else:
        print("✗ Some files or dependencies are missing!")
        print("Please review the errors above.")

    print("\nTo install all dependencies:")
    print("  pip3 install -r requirements.txt")

    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
