# Testing Files Reference

Quick reference for all test files and what they do.

## Automated Tests (Run these yourself)

| File | What it Tests | Runtime | Command |
|------|--------------|---------|---------|
| `verify_project.py` | All files exist, dependencies installed | 5s | `python3 verify_project.py` |
| `test_raw_hid.py` | Raw HID data from YOUR controller | 3s | `python3 test_raw_hid.py` |
| `test_input_processor.py` | Deadzone, curves, smoothing | 2s | `python3 test_input_processor.py` |
| `test_browser_bridge.py` | Gamepad conversion logic | 2s | `python3 test_browser_bridge.py` |
| `test_websocket_integration.py` | WebSocket server + client | 5s | `python3 test_websocket_integration.py` |
| `test_end_to_end.py` | **Complete system test** | 10s | `python3 test_end_to_end.py` |

## Manual Tests (Interactive)

| File | What it Does | How to Use |
|------|-------------|-----------|
| `main.py` | Launch full GUI app | `python3 main.py` |
| `device_manager.py` | List detected controllers | `python3 device_manager.py` |
| `license_validator.py` | Check/activate license | `python3 license_validator.py check` |

## Documentation

| File | Contents |
|------|----------|
| `TESTING_GUIDE.md` | **Complete step-by-step testing guide** |
| `QUICK_START.md` | 5-minute setup guide |
| `ACTUAL_TEST_RESULTS.md` | Real test results with your hardware |
| `TEST_REPORT.md` | Initial component test report |
| `README.md` | Project overview and documentation |

## Recommended Testing Order

### Quick Verification (5 minutes)
```bash
python3 verify_project.py        # Check everything is installed
python3 test_raw_hid.py          # Test YOUR hardware
python3 test_end_to_end.py       # Full integration test
```

### Full Manual Test (15 minutes)
```bash
pip3 install PyQt6               # Install GUI (if needed)
python3 main.py                  # Launch app
# Then follow TESTING_GUIDE.md steps
```

### Just Want to Play? (5 minutes)
See **QUICK_START.md**
