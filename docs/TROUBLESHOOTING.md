# CloudPad Troubleshooting Guide

## Common Launch Issues

### Issue: Import Errors
**Symptoms:** Error about missing modules (PyQt6, hid, websockets)
**Solution:**
```bash
pip3 install -r requirements.txt
```

### Issue: "No module named 'license_validator'"
**Symptoms:** ImportError when starting
**Solution:** Make sure you're in the project directory:
```bash
cd /Users/kutay/Projects/xboxControllerEmulator
python3 cloudpad.py
```

### Issue: GUI doesn't appear
**Symptoms:** Command runs but no window shows
**Solution:** 
1. Check if process is running: `ps aux | grep cloudpad`
2. Kill existing: `killall python3`
3. Try again: `python3 cloudpad.py`

### Issue: "Address already in use" (port 8765)
**Symptoms:** WebSocket server can't start
**Solution:**
```bash
# Find process using port 8765
lsof -i :8765
# Kill it
kill -9 <PID>
```

### Issue: Permission denied on devices
**Symptoms:** Can't access HID devices
**Solution:** On macOS, grant Input Monitoring permission:
1. System Settings → Privacy & Security → Input Monitoring
2. Add Terminal.app or iTerm

### Issue: Qt platform plugin error
**Symptoms:** "qt.qpa.plugin: Could not load the Qt platform plugin"
**Solution:**
```bash
# Reinstall PyQt6
pip3 uninstall PyQt6
pip3 install PyQt6
```

## Debug Mode

Run with verbose output:
```bash
python3 -u cloudpad.py 2>&1 | tee cloudpad_debug.log
```

## Quick Test

Test all components:
```bash
python3 test_suite.py
```

## Getting Help

If issue persists:
1. Run: `python3 test_suite.py` and share output
2. Check `cloudpad_debug.log` for errors
3. Provide exact error message
