#!/bin/bash
# Build script for macOS app bundle

echo "Building CloudPad for macOS..."

# Install PyInstaller if not present
pip3 install pyinstaller

# Clean previous builds
rm -rf build dist

# Build app bundle using PyInstaller script
# We run it from the project root so paths work correctly
cd "$(dirname "$0")/.."
python3 scripts/build_pyinstaller.py

# Check result
if [ -d "dist/CloudPad.app" ]; then
    echo "✓ Build successful: dist/CloudPad.app"
    echo "Size: $(du -sh dist/CloudPad.app | cut -f1)"
    
    # Code sign if Apple Developer certificate is available
    if security find-identity -v -p codesigning | grep -q "Developer ID Application"; then
        echo "Code signing app..."
        codesign --deep --force --verify --verbose --sign "Developer ID Application" dist/CloudPad.app
        echo "✓ App signed"
        
        # Create DMG
        echo "Creating DMG..."
        hdiutil create -volname "CloudPad" -srcfolder dist/CloudPad.app -ov -format UDZO dist/CloudPad.dmg
        echo "✓ DMG created: dist/CloudPad.dmg"
        
        # Notarize (requires Apple Developer account)
        echo "To notarize:"
        echo "  xcrun notarytool submit dist/CloudPad.dmg --apple-id YOUR_EMAIL --team-id TEAM_ID --password APP_PASSWORD --wait"
        echo "  xcrun stapler staple dist/CloudPad.app"
    else
        echo "⚠ No code signing certificate found - app will not be signed"
        echo "  Install Developer ID certificate from https://developer.apple.com"
    fi
else
    echo "✗ Build failed"
    exit 1
fi
