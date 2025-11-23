# CloudPad Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Firefox extension variant
- Comprehensive documentation suite
- Contributing guidelines
- MIT License

### Fixed
- Calibration crashes with DeviceInfo objects
- Raw HID reading for button detection
- String conversion in finish_calibration

## [1.0.0] - 2024-11-23

### Added
- Universal HID device detection and management
- Auto-calibration wizard with real-time button detection
- Raw HID byte reading for device-agnostic input
- WebSocket server for browser communication (port 8765)
- Chrome browser extension for virtual gamepad injection
- Modern dark-themed GUI (PyQt6)
- License system with free and Pro tiers
- Device selection and connection monitoring
- Real-time input activity indicator
- Comprehensive status logging

### Features
- **Free Tier:**
  - Single device support
  - Basic Xbox controller emulation
  - Browser extension(included)
  
- **Pro Tier** ($14.99 one-time):
  - Unlimited devices
  - Multiple profiles
  - Advanced mapping features

### Platforms
- macOS (Intel & Apple Silicon)
- Windows 10/11
- Linux (Ubuntu, Fedora, etc.)

### Supported Cloud Gaming Services
- Xbox Cloud Gaming (xCloud)
- GeForce NOW
- Amazon Luna

### Technical Details
- Built with Python 3.11+
- PyQt6 for GUI
- hidapi for device communication
- WebSockets for browser bridge
- Manifest V3 Chrome extension

### Known Issues
- macOS py2app builds have PyQt6 packaging issues
- Workaround: Use source or PyInstaller build
- Firefox extension not yet released (manifest ready)

### Documentation
- README.md - Quick start guide
- TROUBLESHOOTING.md - Common issues and fixes
- TESTING.md - Comprehensive test scenarios
- FAQ.md - Frequently asked questions
- ROADMAP.md - Future development plans
- CONTRIBUTING.md - Contribution guidelines

### Build Systems
- `build_macos.sh` - macOS app bundle (py2app)
- `build_pyinstaller.py` - Alternative macOS build
- `build_windows.sh` - Windows installer (Inno Setup)
- `build_linux.sh` - Linux AppImage

## [0.9.0] - 2024-11-20 [BETA]

### Added
- Initial prototype with HOTAS Warthog support
- Basic browser bridge
- Command-line calibration tool (`calibrate.py`)
- Simple button mapping JSON storage

### Changed
- Migrated from pygame to hidapi
- Refactored input reader for universality

### Removed
- Hardcoded HOTAS-specific mappings
- Pygame dependency

## [0.1.0] - 2024-11-15 [ALPHA]

### Added
- Proof of concept with Xbox controller passthrough
- Basic DSU server protocol support
- Test HTML page for validation

---

**Legend:**
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for bug fixes
- `Security` for vulnerability fixes
