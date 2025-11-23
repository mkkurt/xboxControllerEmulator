#!/bin/bash
# Build script for Linux AppImage

echo "Building CloudPad for Linux..."

# Install dependencies
pip3 install pyinstaller

# Build standalone executable
pyinstaller --onefile --windowed --name CloudPad \
    --add-data "extension:extension" \
    --hidden-import=hid \
    --hidden-import=websockets \
    --hidden-import=PyQt6 \
    cloudpad.py

# Create AppImage structure
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/256x256/apps

# Copy executable
cp dist/CloudPad AppDir/usr/bin/

# Create desktop entry
cat > AppDir/usr/share/applications/cloudpad.desktop << EOF
[Desktop Entry]
Type=Application
Name=CloudPad
Comment=Universal Controller Emulator
Exec=CloudPad
Icon=cloudpad
Categories=Game;Utility;
Terminal=false
EOF

# Copy icon (if exists)
if [ -f "resources/icon.png" ]; then
    cp resources/icon.png AppDir/usr/share/icons/hicolor/256x256/apps/cloudpad.png
fi

# Download appimagetool if not present
if [ ! -f "appimagetool-x86_64.AppImage" ]; then
    wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
    chmod +x appimagetool-x86_64.AppImage
fi

# Create AppImage
./appimagetool-x86_64.AppImage AppDir CloudPad-x86_64.AppImage

if [ -f "CloudPad-x86_64.AppImage" ]; then
    echo "✓ AppImage created: CloudPad-x86_64.AppImage"
    echo "Size: $(du -h CloudPad-x86_64.AppImage | cut -f1)"
else
    echo "✗ AppImage creation failed"
    exit 1
fi
