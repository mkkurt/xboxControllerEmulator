# CloudPad End-to-End Testing Guide

## Test Scenarios

### 1. Device Detection
**Steps:**
1. Launch CloudPad
2. Observe "Connected Devices" panel
3. Connect/disconnect controller
4. Verify dynamic device list updates

**Expected:**
- ✅ Devices appear immediately
- ✅ Device name shows correctly
- ✅ VID:PID displayed

### 2. Calibration Workflow
**Steps:**
1. Click "Auto-Calibrate"
2. Follow on-screen prompts
3. Press each requested button
4. Complete calibration

**Expected:**
- ✅ Calibration dialog opens
- ✅ HID device opens successfully
- ✅ Button presses detected in realtime
- ✅ Config file saved
- ✅ No crashes

**Test Devices:**
- [x] Thrustmaster HOTAS Warthog
- [ ] Logitech G29 Racing Wheel
- [ ] Xbox Controller (baseline)
- [ ] Generic USB Joystick

### 3. Emulation Start/Stop
**Steps:**
1. Start emulation
2. Move controller axes
3. Press buttons
4. Observe activity indicator
5. Stop emulation

**Expected:**
- ✅ WebSocket server starts (port 8765)
- ✅ Input reader thread starts
- ✅ Activity bar shows input
- ✅ Clean shutdown

### 4. Browser Extension Integration
**Steps:**
1. Click "Browser Extension"
2. Open extension folder
3. Load in Chrome
4. Visit Xbox Cloud Gaming
5. Start CloudPad emulation
6. Observe gamepad API

**Expected:**
- ✅ Extension installs without errors
- ✅ Content script injects
- ✅ Virtual gamepad appears
- ✅ Inputs register in game

**Test Platforms:**
- [ ] Xbox Cloud Gaming
- [ ] GeForce NOW
- [ ] Amazon Luna

### 5. License System
**Steps:**
1. Click "License" button
2. Try invalid key
3. Try valid Pro key
4. Verify Pro features unlock

**Expected:**
- ✅ License dialog opens
- ✅ Invalid key rejected
- ✅ Valid key accepted
- ✅ Status bar updates

### 6. Multi-Device Support (Pro)
**Steps:**
1. Activate Pro license
2. Connect 2+ devices
3. Switch between devices
4. Test simultaneous input

**Expected:**
- ✅ All devices detected
- ✅ Can calibrate multiple
- ✅ Switch devices seamlessly

### 7. Build Verification
**Steps:**
1. Build macOS app
2. Launch bundled app
3. Test all features
4. Verify no missing dependencies

**Command:**
```bash
./build_macos.sh
open dist/CloudPad.app
```

**Expected:**
- ✅ App launches
- ✅ All features work
- ✅ HID devices accessible
- ✅ No import errors

### 8. Cross-Platform Verification
**Platforms:**
- [x] macOS (Intel)
- [ ] macOS (Apple Silicon)
- [ ] Windows 10/11
- [ ] Ubuntu Linux
- [ ] Fedora Linux

### 9. Performance Testing
**Metrics:**
- Input latency: < 16ms
- CPU usage: < 5%
- Memory usage: < 200MB
- WebSocket throughput: > 1000 messages/sec

**Tools:**
```bash
# Monitor performance
top | grep CloudPad
```

### 10. Error Handling
**Scenarios:**
- Device disconnected mid-calibration
- Port 8765 already in use
- Invalid config file
- No devices connected
- Permission denied (HID access)

**Expected:**
- ✅ Graceful error messages
- ✅ No crashes
- ✅ Clear user guidance

## Regression Testing

After any code change, verify:
1. Calibration still works
2. Emulation starts/stops
3. Extension connects
4. No new crashes

## Automated Testing

```bash
# Run full test suite
python3 test_suite.py

# Expected output:
# ✓ Device detection: PASS
# ✓ License validation: PASS
# ✓ Universal reader: PASS
# ✓ Browser bridge: PASS
# ✓ Extension files: PASS
```

## Known Issues

1. **macOS Build - PyQt6 Packaging**
   - Status: In Progress
   - Workaround: Use source or PyInstaller
   
2. **Firefox Extension**
   - Status: TODO
   - Chrome extension works

## Test Reports

Use this template for reporting test results:

```markdown
# Test Report - [Date]

**Tester:** [Name]
**Version:** [Version]
**Platform:** [OS]

## Results
- Device Detection: ✅/❌
- Calibration: ✅/❌
- Emulation: ✅/❌
- Extension: ✅/❌
- License: ✅/❌

## Issues Found
1. [Issue description]
2. [Issue description]

## Notes
[Additional observations]
```
