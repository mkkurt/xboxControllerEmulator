# CloudPad - Frequently Asked Questions (FAQ)

## General Questions

### What is CloudPad?
CloudPad is a universal controller emulator that transforms ANY HID-compatible controller into an Xbox controller for cloud gaming platforms. It works with HOTAS, racing wheels, flight sticks, and any USB game controller.

### Which platforms does it support?
- ✅ Xbox Cloud Gaming (xCloud)
- ✅ GeForce NOW
- ✅ Amazon Luna
- Works on Windows, macOS, and Linux

### Is it free?
Yes! CloudPad has a free tier that supports single-device emulation. Pro features (unlimited devices, advanced mapping) are available for a one-time purchase of $14.99.

### Do I need technical knowledge?
No! CloudPad features auto-calibration - just click Auto-Calibrate and press each button when prompted. The whole process takes less than a minute.

## Technical Questions

### How does it work?
1. CloudPad reads input from your controller using HID (Human Interface Device) protocol
2. Translates inputs to Xbox controller format in realtime
3. Sends data to browser via WebSocket
4. Browser extension injects a virtual Xbox gamepad
5. Cloud gaming platform sees a standard Xbox controller

### What controllers are supported?
ANY HID-compatible USB controller including:
- HOTAS systems (Thrustmaster, Logitech, etc.)
- Racing wheels (G29, T300, etc.)
- Flight sticks
- Generic USB joysticks
- Even custom/DIY controllers

### What about latency?
CloudPad introduces < 1ms of latency. Your bottleneck will be your internet connection to the cloud gaming service, not CloudPad.

### Can I use multiple controllers at once?
With CloudPad Pro, yes! You can have multiple controller profiles and switch between them instantly.

## Setup Questions

### How do I install the browser extension?
1. Click "Browser Extension" in CloudPad
2. Click "Open Extension Folder"
3. Open Chrome and go to `chrome://extensions/`
4. Enable "Developer mode" (toggle top-right)
5. Click "Load unpacked"
6. Select the extension folder that opened

### My controller isn't detected. What do I do?
1. Make sure it's plugged in via USB (Bluetooth not supported yet)
2. On macOS: Grant Input Monitoring permission in System Settings
3. Try disconnecting and reconnecting
4. Check if it appears in System Settings → Game Controllers (macOS)

### Calibration keeps failing. Help!
1. Make sure you're pressing physical buttons, not moving axes
2. Try a different button if one doesn't register
3. Use "Skip This Button" for unmapped buttons
4. Check HID permissions in System Settings

### The browser extension isn't working
1. Make sure CloudPad is running and emulation is started
2. Refresh the cloud gaming page
3. Check if the extension is enabled in Chrome
4. Look for the CloudPad icon - it should show "Connected" in green

## Troubleshooting

### "Permission denied" error on macOS
macOS re

quires Input Monitoring permission:
1. System Settings → Privacy & Security → Input Monitoring
2. Add Terminal.app or your browser
3. Restart CloudPad

### "Port 8765 already in use"
Another instance of CloudPad is running:
1. Quit all CloudPad instances
2. Run: `lsof -i :8765` to find the process
3. Kill it: `kill -9 <PID>`
4. Restart CloudPad

### WebSocket connection fails
1. Check firewall isn't blocking port 8765
2. Try restarting browser
3. Disable other gamepad-related extensions
4. Check browser console for errors (F12)

### Built app won't open on macOS
Currently known issue with py2app packaging. Workaround:
```bash
# Run from source
cd /path/to/CloudPad
python3 cloudpad.py
```

A fixed build with PyInstaller is coming soon.

## Pro Features

### What do I get with CloudPad Pro?
- Unlimited device support
- Multiple controller profiles
- Advanced mapping (macros, axis curves, deadzones)
- Priority email support
- Early access to new features

### Is it a subscription?
No! $14.99 is a one-time purchase. Own it forever.

### How do I activate my Pro license?
1. Purchase from Gumroad
2. Receive license key via email
3. Open CloudPad → Click "License"
4. Enter email and license key
5. Click "Activate"

### Can I use my license on multiple computers?
Yes! One license works on all your personal devices.

## Privacy & Security

### Does CloudPad collect data?
No. CloudPad runs 100% locally. No analytics, no telemetry, no data collection.

### Does it require internet?
Only to play cloud games. CloudPad itself works offline.

### Is my controller data safe?
Yes. All input data stays on your local machine. CloudPad never sends data to external servers.

## Platform-Specific

### macOS - "App is damaged" error
Right-click → Open (instead of double-clicking) to bypass Gatekeeper on first launch.

### Windows - SmartScreen warning
Click "More info" → "Run anyway". The app will be code-signed in future versions.

### Linux - Permission denied
Add your user to the input group:
```bash
sudo usermod -a -G input $USER
```
Then log out and back in.

## Still Have Questions?

- 📧 Email: support@cloudpad.app
- 💬 Discord: https://discord.gg/cloudpad
- 📖 Docs: https://docs.cloudpad.app
- 🐛 Report bugs: https://github.com/yourname/cloudpad/issues

---

**Can't find your answer?** Ask on Discord - our community is super helpful!
