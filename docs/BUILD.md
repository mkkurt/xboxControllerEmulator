# CloudPad Build Instructions

## Prerequisites

### All Platforms
```bash
pip3 install -r requirements.txt
```

### Windows
- PyInstaller: `pip install pyinstaller`
- Inno Setup: Download from https://jrsoftware.org/isdl.php

### macOS
- py2app: `pip3 install py2app`
- Apple Developer account (for code signing)
- Xcode Command Line Tools

### Linux
- PyInstaller: `pip install pyinstaller`
- appimagetool (auto-downloaded by build script)

---

## Building

### Windows

```bash
# Build executable
./build_windows.sh

# Or manually:
pyinstaller cloudpad_windows.spec --clean

# Create installer (Windows only):
iscc installer_windows.iss
```

**Output:**
- `dist/CloudPad.exe` - Standalone executable
- `Output/CloudPad_Setup.exe` - Installer (if Inno Setup run)

---

### macOS

```bash
./build_macos.sh

# Or manually:
python3 setup.py py2app

# Code sign (if you have Developer ID):
codesign --deep --force --sign "Developer ID Application" dist/CloudPad.app

# Create DMG:
hdiutil create -volname "CloudPad" -srcfolder dist/CloudPad.app -ov -format UDZO dist/CloudPad.dmg

# Notarize (requires Apple ID):
xcrun notarytool submit dist/CloudPad.dmg --apple-id YOUR_EMAIL --team-id TEAM_ID --wait
xcrun stapler staple dist/CloudPad.app
```

**Output:**
- `dist/CloudPad.app` - macOS application bundle
- `dist/CloudPad.dmg` - DMG installer

---

### Linux

```bash
./build_linux.sh

# Or manually with PyInstaller:
pyinstaller --onefile --windowed --name CloudPad cloudpad.py
```

**Output:**
- `CloudPad-x86_64.AppImage` - Universal Linux app
- `dist/CloudPad` - Standalone executable

---

## Testing Builds

### macOS (current platform)
```bash
# Test app bundle
open dist/CloudPad.app

# Test from command line
./dist/CloudPad.app/Contents/MacOS/CloudPad
```

### Windows (requires Windows machine or VM)
```bash
# Just run the .exe
CloudPad.exe
```

### Linux (requires Linux machine or VM)
```bash
# Make AppImage executable and run
chmod +x CloudPad-x86_64.AppImage
./CloudPad-x86_64.AppImage
```

---

## Distribution Checklist

- [ ] Build for all 3 platforms
- [ ] Test each build on target OS
- [ ] Code sign macOS app
- [ ] Create release notes
- [ ] Upload to Gumroad
- [ ] Update download links in marketing materials
- [ ] Submit browser extension to Chrome Web Store

---

## Troubleshooting

**"Module not found" errors:**
- Add to `hiddenimports` in .spec file
- Or add to `packages` in setup.py

**macOS "App is damaged":**
- App needs to be code signed
- Run: `xattr -cr CloudPad.app`

**Windows SmartScreen warning:**
- Expected for unsigned apps
- Users must click "More info" → "Run anyway"
- Get code signing certificate to avoid

**Linux permission denied:**
- Run: `chmod +x CloudPad-x86_64.AppImage`
