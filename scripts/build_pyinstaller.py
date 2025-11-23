# CloudPad - macOS PyInstaller Build Script

import PyInstaller.__main__
import os
import sys

# Get project directory (parent of scripts/)
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)

# Change to project directory
os.chdir(project_dir)

# Build parameters
PyInstaller.__main__.run([
    'main.py',
    '--name=CloudPad',
    '--windowed',
    '--noconfirm',
    '--clean',
    # '--icon=resources/icon.icns', # Uncomment if icon exists
    '--add-data=extension:extension',
    '--exclude-module=PyQt6.QtBluetooth',
    '--exclude-module=PyQt6.QtNfc',
    '--exclude-module=PyQt6.QtPositioning',
    '--exclude-module=PyQt6.QtSensors',
    '--exclude-module=PyQt6.QtSerialPort',
    '--exclude-module=PyQt6.QtSql',
    '--exclude-module=PyQt6.QtTest',
    '--exclude-module=PyQt6.QtXml',
    '--exclude-module=PyQt6.QtMultimedia',
    '--exclude-module=PyQt6.QtQuick',
    '--exclude-module=PyQt6.QtQml',
    '--exclude-module=tkinter',
    '--exclude-module=matplotlib',
    '--exclude-module=numpy',
    '--hidden-import=PyQt6.QtCore',
    '--hidden-import=PyQt6.QtGui',
    '--hidden-import=PyQt6.QtWidgets',
    # '--collect-all=PyQt6', # Causes issues with QtBluetooth framework on macOS
    '--noconfirm',
    '--clean',
    f'--distpath={os.path.join(project_dir, "dist")}',
    f'--workpath={os.path.join(project_dir, "build")}',
])

print("\n✓ PyInstaller build complete!")
print(f"App bundle: {os.path.join(project_dir, 'dist', 'CloudPad.app')}")
