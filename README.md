# CloudPad - Complete Project README

![CloudPad Logo](docs/logo.png)

# CloudPad - Universal Controller Emulator for Cloud Gaming

Transform ANY controller into an Xbox controller for cloud gaming platforms. Works with HOTAS, racing wheels, flight sticks, and any HID device.

## 🎮 Features

- **Universal Device Support** - Works with ANY HID controller
- **Auto-Calibration** - Automatically map buttons in seconds
- **Cross-Platform** - Windows, macOS, Linux
- **Browser Extension** - Seamless integration with cloud gaming
- **Zero Latency** - Direct input processing
- **Free & Pro Tiers** - Freemium model

## 🚀 Quick Start

### Installation

**macOS:**
```bash
# Download and open CloudPad.app
open CloudPad.app
```

**Windows:**
```bash
# Download and run installer
CloudPad_Setup.exe
```

**Linux:**
```bash
# Download AppImage
chmod +x CloudPad-x86_64.AppImage
./CloudPad-x86_64.AppImage
```

### First Use

1. **Connect Your Controller**
   - Plug in any USB controller (HOTAS, racing wheel, etc.)

2. **Auto-Calibrate**
   - Click "Auto-Calibrate" button
   - Follow on-screen instructions
   - Press each button when prompted

3. **Install Browser Extension**
   - Click "Browser Extension" button
   - Follow installation instructions
   - Load unpacked extension in Chrome

4. **Start Playing**
   - Click "Start Emulation"
   - Visit Xbox Cloud Gaming or GeForce NOW
   - Your controller is now an Xbox controller!

## 🌐 Supported Platforms

- ✅ Xbox Cloud Gaming (xCloud)
- ✅ GeForce NOW
- ✅ Amazon Luna
- ✅ Google Stadia (sunset)

## 💰 Pricing

**Free Tier:**
- Single device support
- Basic Xbox emulation
- Browser extension

**Pro Tier ($14.99 one-time):**
- Unlimited devices
- Multi-device profiles
- Advanced mapping (macros, curves, deadzones)
- Priority support

## 🛠️ Development

### Running from Source

```bash
# Install dependencies
pip3 install -r requirements.txt

# Run app
python3 main.py
```

### Building

**macOS:**
```bash
./build_macos.sh
```

**Windows:**
```bash
./build_windows.sh
```

**Linux:**
```bash
./build_linux.sh
```

## 📁 Project Structure

```
cloudpad/
├── main.py                  # Main application entry point
├── device_manager.py        # HID device detection
├── universal_reader.py      # Input reading
├── browser_bridge.py        # WebSocket server
├── input_processor.py       # Advanced input processing
├── dsu_server.py           # DSU protocol server
├── license_validator.py     # License system
├── ui/                      # GUI components
│   ├── main_window.py
│   ├── calibration_dialog.py
│   └── ...
├── extension/               # Browser extension
│   ├── manifest.json
│   ├── content.js
│   └── popup.html
├── presets/                 # Device presets
└── build_macos.sh          # macOS build script
```

## 🧪 Testing

```bash
# Run test suite
python3 test_suite.py
```

## 🐛 Troubleshooting

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues.

## 📄 License

Proprietary - See LICENSE file

## 🤝 Support

- Email: support@cloudpad.app
- Docs: https://docs.cloudpad.app
- Discord: https://discord.gg/cloudpad

## 🙏 Credits

Created by [Your Name]

Powered by:
- PyQt6 for GUI
- hidapi for device communication
- websockets for browser bridge

---

**CloudPad** - Use ANY controller with cloud gaming. © 2024
