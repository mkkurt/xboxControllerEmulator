# CloudPad vs Alternatives - Comparison Guide

## Quick Comparison Table

| Feature | CloudPad | vJoy | UCR | reWASD | Controller Companion |
|---------|----------|------|-----|--------|---------------------|
| **Price** | Free / $15 Pro | Free | Free | $7 | $3 |
| **Cloud Gaming** | ✅ Built-in | ❌ Manual | ❌ Manual | ❌ No | ❌ No |
| **Auto-Calibration** | ✅ 60 sec | ❌ Manual | ❌ Manual | ❌ Manual | ❌ Manual |
| **Universal HID** | ✅ ANY device | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited | ⚠️ Limited |
| **Browser Extension** | ✅ Included | ❌ No | ❌ No | ❌ No | ❌ No |
| **Cross-Platform** | Win/Mac/Linux | Win only | Win only | Win only | Win only |
| **Open Source** | ✅ MIT | ✅ GPL | ✅ MIT | ❌ Proprietary | ❌ Proprietary |
| **Latency** | <1ms | ~2ms | ~3ms | ~2ms | ~5ms |
| **Setup Time** | 60 seconds | 30+ min | 45+ min | 20+ min | 15+ min |
| **Privacy** | Local only | Local only | Local only | Unknown | Telemetry |
| **Support** | Discord/Email | Forums | GitHub | Email | Email |
| **Last Updated** | 2024 | 2024 | 2023 | 2024 | 2022 |

---

## Detailed Comparisons

### CloudPad vs vJoy

**vJoy** is a virtual joystick driver for Windows.

**Advantages of CloudPad:**
- ✅ Works on Mac and Linux (vJoy is Windows-only)
- ✅ Built-in browser extension for cloud gaming
- ✅ Auto-calibration wizard (vJoy requires manual configuration)
- ✅ Modern GUI interface
- ✅ Designed specifically for cloud gaming

**Advantages of vJoy:**
- ✅ Completely free (no Pro tier)
- ✅ More established (10+ years old)
- ✅ Deeper DirectInput integration on Windows

**Use Case:**
- Choose **CloudPad** for cloud gaming, Mac/Linux, ease of setup
- Choose **vJoy** for local Windows games, complex multi-device setups

---

### CloudPad vs UCR (Universal Control Remapper)

**UCR** is an open-source controller remapping tool.

**Advantages of CloudPad:**
- ✅ Cross-platform (UCR is Windows-only)
- ✅ Cloud gaming focus with browser extension
- ✅ Auto-calibration (UCR requires manual scripting)
- ✅ Modern PyQt6 interface
- ✅ Active development

**Advantages of UCR:**
- ✅ More granular control over mappings
- ✅ Scripting capabilities (AutoHotkey-based)
- ✅ Completely free

**Use Case:**
- Choose **CloudPad** for cloud gaming, simplicity, cross-platform
- Choose **UCR** for local games, advanced scripting, Windows power users

---

### CloudPad vs reWASD

**reWASD** is a commercial controller remapping tool.

**Advantages of CloudPad:**
- ✅ Open source (reWASD is proprietary)
- ✅ Cross-platform (reWASD is Windows-only)
- ✅ Cloud gaming browser extension
- ✅ Privacy-focused (no telemetry)
- ✅ One-time $15 vs reWASD's $7 (but CloudPad has free tier)

**Advantages of reWASD:**
- ✅ More mature product (years of development)
- ✅ Advanced features (turbo, combos, profiles)
- ✅ Better axis/curve customization (currently)
- ✅ Gyro support

**Use Case:**
- Choose **CloudPad** for cloud gaming, Mac/Linux, open source preference
- Choose **reWASD** for Windows-only advanced local gaming

---

### CloudPad vs Controller Companion

**Controller Companion** is a Steam-focused controller tool.

**Advantages of CloudPad:**
- ✅ Cloud gaming focus (CC is Steam/desktop)
- ✅ Cross-platform
- ✅ Universal HID support
- ✅ Active development (CC last updated 2022)
- ✅ Open source

**Advantages of Controller Companion:**
- ✅ Cheaper ($3 vs $15)
- ✅ Steam integration
- ✅ Desktop navigation features

**Use Case:**
- Choose **CloudPad** for cloud gaming, HID devices, modern platform
- Choose **Controller Companion** for Steam Big Picture, desktop navigation

---

## Why CloudPad Stands Out

### 1. Cloud Gaming First
Every other tool was built for local games. CloudPad is purpose-built for cloud gaming:
- Browser extension for seamless integration
- WebSocket bridge (not virtual device drivers)
- Gamepad API injection
- Optimized for streaming latency

### 2. Universal Auto-Calibration
Other tools require:
- Manual button mapping
- Configuration file editing
- Understanding of HID reports
- Trial and error

CloudPad:
- 60-second wizard
- Just press buttons when asked
- Works with ANY HID device
- No technical knowledge needed

### 3. True Cross-Platform
Most tools are Windows-only. CloudPad works on:
- Windows 10/11
- macOS 10.13+
- Linux (Ubuntu, Fedora, etc.)

Same features, same experience everywhere.

### 4. Open Source & Privacy
- MIT licensed codebase
- No telemetry or tracking
- Community-driven development
- Transparent functionality

You own your data. You control your software.

### 5. Modern Technology Stack
- Python + PyQt6 (not legacy .NET/WinForms)
- WebSockets (not clunky virtual drivers)
- Browser extensions (not registry hacks)
- Active development (not abandoned)

---

## Migration Guides

### From vJoy to CloudPad

1. Uninstall vJoy virtual devices (optional, they won't conflict)
2. Download CloudPad for your platform
3. Run auto-calibration for your controller
4. Install browser extension
5. Start gaming!

**Time:** ~5 minutes

### From UCR to CloudPad

1. Export your UCR mappings (for reference)
2. Install CloudPad
3. Calibrate  (CloudPad will learn your layout)
4. Compare to UCR config to verify
5. Done!

**Time:** ~10 minutes

### From reWASD to CloudPad

1. Note your current button mappings
2. Install CloudPad
3. Run calibration (map same buttons to same functions)
4. Test in cloud gaming
5. Keep reWASD for local games if you want advanced features

**Time:** ~5 minutes

---

## Feature Comparison Matrix

### Input Support

| Feature | CloudPad | vJoy | UCR | reWASD |
|---------|----------|------|-----|--------|
| Buttons | ✅ | ✅ | ✅ | ✅ |
| Axes | ✅ | ✅ | ✅ | ✅ |
| D-Pad | ✅ | ✅ | ✅ | ✅ |
| Triggers | ✅ | ✅ | ✅ | ✅ |
| Gyro | ⏳ v1.3 | ❌ | ❌ | ✅ |
| Touchpad | ⏳ v2.0 | ❌ | ❌ | ✅ |

### Configuration

| Feature | CloudPad | vJoy | UCR | reWASD |
|---------|----------|------|-----|--------|
| Auto-calibration | ✅ | ❌ | ❌ | ❌ |
| Profile saving | ✅ | ⚠️ | ✅ | ✅ |
| Profile sharing | ✅ Pro | ❌ | ⚠️ | ✅ |
| Per-game profiles | ⏳ v1.2 | ⚠️ | ✅ | ✅ |
| Macros | ⏳ v1.2 | ❌ | ✅ | ✅ |
| Axis curves | ⏳ v1.2 | ⚠️ | ✅ | ✅ |

### Platform Support

| Platform | CloudPad | vJoy | UCR | reWASD |
|----------|----------|------|-----|--------|
| Windows | ✅ | ✅ | ✅ | ✅ |
| macOS | ✅ | ❌ | ❌ | ❌ |
| Linux | ✅ | ❌ | ❌ | ❌ |
| Chrome | ✅ | ❌ | ❌ | ❌ |
| Firefox | ⏳ v1.1 | ❌ | ❌ | ❌ |

---

## Frequently Asked Questions

### Can I use CloudPad with local games?
CloudPad is optimized for cloud gaming but works with local browser-based games. For native PC games, tools like vJoy or reWASD may be better suited.

### Why not just use vJoy?
vJoy is Windows-only and requires manual configuration. CloudPad works on all platforms and has 60-second auto-calibration. Plus, the browser extension makes cloud gaming seamless.

### Is CloudPad better than reWASD?
For cloud gaming: yes. For local Windows games with advanced features: reWASD may be better. They serve different use cases.

### Can I use CloudPad alongside other tools?
Generally yes, though virtual device drivers may conflict. CloudPad uses a different approach (WebSocket + browser extension) so conflicts are rare.

### Which tool should I choose?

**Choose CloudPad if:**
- You play cloud games (xCloud, GeForce NOW, Luna)
- You use Mac or Linux
- You want simple setup (60 seconds)
- You value open source and privacy

**Choose vJoy if:**
- Windows-only local gaming
- You need complex multi-device setups
- You're comfortable with manual configuration

**Choose reWASD if:**
- Windows-only local gaming
- You want advanced features (gyro, macros, profiles)
- You're willing to pay and sacrifice open source

**Choose UCR if:**
- Windows-only
- You want scripting capabilities
- You're technical and want granular control

---

## Bottom Line

CloudPad is the **only tool purpose-built for cloud gaming** with cross-platform support and universal auto-calibration.

For cloud gaming specifically, nothing else comes close.

For local Windows gaming with advanced features, reWASD or UCR might be better suited.

**Try CloudPad free** and see if it meets your needs. The Pro upgrade is optional and inexpensive ($15 one-time).

---

*Have questions? Join our Discord or email support@cloudpad.app*
