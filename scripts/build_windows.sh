#!/bin/bash
# Build script for Windows (run on Windows or cross-compile)

echo "Building CloudPad for Windows..."

# Install PyInstaller if not present
pip install pyinstaller

# Build executable
pyinstaller cloudpad_windows.spec --clean

# Check result
if [ -f "dist/CloudPad.exe" ]; then
    echo "✓ Build successful: dist/CloudPad.exe"
    echo "Size: $(du -h dist/CloudPad.exe | cut -f1)"
else
    echo "✗ Build failed"
    exit 1
fi

# Optional: Create installer with Inno Setup (Windows only)
if command -v iscc &> /dev/null; then
    echo "Creating installer..."
    iscc installer_windows.iss
    echo "✓ Installer created: Output/CloudPad_Setup.exe"
fi
