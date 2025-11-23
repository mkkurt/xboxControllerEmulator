# CloudPad - Manual Testing Guide

**Complete step-by-step guide to test your CloudPad installation**

---

## Prerequisites

### Required Dependencies
```bash
# Install PyQt6 for GUI (required for full testing)
pip3 install PyQt6

# Verify all dependencies are installed
pip3 install -r requirements.txt

# Check installation
python3 verify_project.py
```

---

## Quick Test Suite (5 minutes)

Run these automated tests to verify everything works:

```bash
# Test 1: Hardware detection
python3 device_manager.py

# Test 2: Raw HID data from your controllers
python3 test_raw_hid.py

# Test 3: Input processing
python3 test_input_processor.py

# Test 4: Browser bridge
python3 test_browser_bridge.py

# Test 5: WebSocket integration
python3 test_websocket_integration.py

# Test 6: End-to-end (comprehensive)
python3 test_end_to_end.py
```

**Expected:** All tests should show ✓ marks and report success.

---

## Full Application Test (10 minutes)

### Step 1: Launch the GUI Application

```bash
# Start CloudPad
python3 main.py
```

**Expected:**
- A window titled "CloudPad - Universal Controller Emulator" appears
- You see "🎮 CloudPad" at the top
- Two panels: "Connected Devices" and "Status"
- Several buttons at the bottom

**If it fails:** Make sure PyQt6 is installed: `pip3 install PyQt6`

---

### Step 2: Detect Your Controllers

1. **Connect your controller** (USB)

2. **Click "🔄 Refresh" button** in the app

**Expected:**
- Your controller appears in the "Connected Devices" list
- Shows format: `✗ Thrustmaster HOTAS Warthog (044f:0402)` or similar
- ✗ = not configured, ✓ = configured

**If nothing appears:**
- Check USB connection
- Try unplugging and replugging
- Check Activity Log for errors

---

### Step 3: Calibrate Your Controller

1. **Select your controller** in the device list (click on it)

2. **Click "⚙ Auto-Calibrate" button**

3. **Follow the calibration wizard:**

   **Stage 1: Axis Range Calibration**
   - Move all sticks in full circles
   - Press all triggers fully
   - Click "Next" when done

   **Stage 2: Axis Mapping**
   - When prompted "Move/Press: Left Stick X", move that axis
   - The wizard will auto-detect which byte is changing
   - Repeat for all axes (Left/Right sticks, triggers)
   - Click "Skip" for axes you don't have

   **Stage 3: Button Mapping**
   - When prompted "Press button: A", press a button you want to map to A
   - The wizard will auto-detect which button you pressed
   - Repeat for all Xbox buttons (A, B, X, Y, LB, RB, etc.)
   - Click "Skip" for buttons you don't have

4. **Click "Finish"**

**Expected:**
- "Calibration Complete!" message
- Your device now shows ✓ instead of ✗
- Configuration saved to `~/Library/Application Support/CloudPad/devices.json`

**Troubleshooting:**
- If wizard can't detect axis movement: Move the axis more dramatically
- If wizard can't detect buttons: Make sure you're pressing hard enough
- If calibration fails: Close and restart the app, try again

---

### Step 4: Test Controller Input

1. **Click "🎮 Test Input" button**

2. **Move your controller** - sticks, triggers, buttons

**Expected:**
- A visual controller diagram appears
- Sticks move as you move them
- Buttons light up when pressed
- Triggers show as bars filling up

**This proves:** Your controller is being read correctly!

---

### Step 5: Start Emulation

1. **Click "▶ Start Emulation" button**

**Expected:**
- Button changes to "⏹ Stop Emulation" (red)
- Status shows "Status: Running - Waiting for browser connection"
- Activity Log shows:
  - "Started input reader"
  - "Started browser bridge on ws://127.0.0.1:8765"
  - "✓ Emulation started!"

**This proves:** The backend is running and ready for browser connections!

---

## Browser Extension Test (5 minutes)

### Step 6: Load the Extension in Chrome

1. **Open Chrome** and go to `chrome://extensions/`

2. **Enable "Developer mode"** (toggle in top-right corner)

3. **Click "Load unpacked"**

4. **Navigate to** and select:
   ```
   /Users/kutay/Projects/xboxControllerEmulator/extension
   ```

5. **Click "Select"**

**Expected:**
- Extension appears in list: "CloudPad Bridge"
- Shows icon and version 1.0.0
- No errors

**Troubleshooting:**
- If you see errors about missing icons: They should exist now (we created them)
- If manifest errors: Check that manifest.json is valid

---

### Step 7: Test Extension Connection

1. **Make sure CloudPad app is running** with "Emulation started"

2. **Open a new tab** in Chrome

3. **Open Developer Console** (F12 or Cmd+Option+I)

4. **Go to any website** (even google.com works for testing)

**Expected in Console:**
```
CloudPad: Initializing...
CloudPad: Connected to local app
CloudPad: Virtual gamepad injected!
```

You should see a green notification in top-right: "CloudPad connected!"

**Troubleshooting:**
- If "Connection failed": Make sure CloudPad app is running with emulation started
- If no messages: Extension might not be active on that page
- Try refreshing the page

---

### Step 8: Test Gamepad API

**In the browser console, type:**

```javascript
// Check if gamepad is detected
navigator.getGamepads()
```

**Expected output:**
```javascript
[
  {
    id: "CloudPad Virtual Xbox Controller",
    index: 0,
    connected: true,
    mapping: "standard",
    axes: [0, 0, 0, 0],
    buttons: [{pressed: false, value: 0}, ...]
  }
]
```

**Now move your controller** and check again:
```javascript
navigator.getGamepads()[0].axes
// Should show your stick positions: [0.5, -0.3, 0, 0]

navigator.getGamepads()[0].buttons[0]
// Press A button, should show: {pressed: true, value: 1}
```

**This proves:** The browser can see your controller as an Xbox gamepad!

---

## Cloud Gaming Test (Optional)

### Step 9: Test with Xbox Cloud Gaming

1. **Go to** https://www.xbox.com/play

2. **Sign in** to your Xbox account

3. **Open developer console** (F12) and check for CloudPad messages

4. **Start any game**

5. **Move your controller**

**Expected:**
- Game responds to your input
- Your HOTAS/custom controller works like an Xbox controller
- Buttons mapped during calibration work correctly

**Note:** You need an Xbox Game Pass Ultimate subscription for this.

---

## Advanced Testing

### Test DSU Server (for emulators)

```bash
# In CloudPad, there's currently no GUI button for DSU
# But you can test it programmatically:
python3 test_dsu_server.py
```

This would let you use your controller with emulators like Cemu, RPCS3, etc.

---

## Troubleshooting Common Issues

### "No controllers detected"
**Solution:**
1. Check USB connection
2. Try different USB port
3. Unplug/replug controller
4. Run: `python3 device_manager.py` to see if it's detected at all

### "Calibration wizard doesn't detect movement"
**Solution:**
1. Move axes more dramatically
2. Make sure controller is USB connected (not wireless)
3. Check if raw data is flowing: `python3 test_raw_hid.py`

### "Browser can't connect to CloudPad"
**Solution:**
1. Make sure CloudPad app is running
2. Make sure you clicked "Start Emulation"
3. Check firewall settings
4. Check if port 8765 is blocked: `lsof -i :8765`

### "Extension won't load"
**Solution:**
1. Make sure you selected the `extension` folder, not a file
2. Check Developer Mode is enabled
3. Look for specific error messages
4. Icons should exist: `ls -la extension/*.png`

### "Game doesn't respond to input"
**Solution:**
1. Make sure you calibrated the controller
2. Check Test Input dialog - does it show movement?
3. Verify WebSocket connection in console
4. Try refreshing the game page

---

## Verification Checklist

Use this to confirm everything works:

- [ ] CloudPad app launches without errors
- [ ] Controller appears in device list
- [ ] Calibration wizard completes successfully
- [ ] Test Input shows visual feedback
- [ ] Emulation starts successfully
- [ ] Browser extension loads without errors
- [ ] Extension connects to CloudPad (green notification)
- [ ] `navigator.getGamepads()` shows CloudPad controller
- [ ] Moving controller updates gamepad values
- [ ] Button presses register in browser
- [ ] (Optional) Cloud gaming works with controller

---

## Getting Help

If something doesn't work:

1. **Check the logs** in CloudPad app's Activity Log
2. **Run diagnostics**: `python3 verify_project.py`
3. **Check test output** from the automated tests
4. **Look at console** for error messages

### Useful diagnostic commands:

```bash
# Check which devices are detected
python3 device_manager.py

# Check if raw data flows
python3 test_raw_hid.py

# Check configuration
cat ~/Library/Application\ Support/CloudPad/devices.json

# Check if WebSocket works
python3 test_websocket_integration.py

# Full system test
python3 test_end_to_end.py
```

---

## Expected Time Investment

- **Quick automated tests:** 5 minutes
- **GUI app + calibration:** 10 minutes
- **Browser extension setup:** 5 minutes
- **Full cloud gaming test:** 5-10 minutes
- **Total:** 25-30 minutes for complete verification

---

## Success Criteria

You've successfully tested CloudPad when:

✅ You can see your controller in the app
✅ You can complete calibration
✅ Test Input shows your controller moving
✅ Browser console shows "CloudPad connected!"
✅ `navigator.getGamepads()` shows your controller
✅ Cloud gaming responds to your input

**At that point, CloudPad is working 100%!**
