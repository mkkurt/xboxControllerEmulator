# Button Detection Fix

## Problem
Button presses were not being detected during calibration.

## Root Causes

### 1. **Baseline Timing Issue**
The baseline was being set too early or when buttons might already be pressed. This caused:
- If a button was already pressed when baseline was captured, pressing it again showed no change
- Baseline wasn't fresh for each button detection

### 2. **Threshold Too High**
The detection threshold was set to 3 units of change, but some buttons only change by 1 bit:
- `0x00` → `0x01` (only 1 unit difference)
- This is completely valid for simple on/off buttons

### 3. **Axis Interference**
Axes that were mapped (but maybe not in detected_axes) could still be changing and confusing button detection.

---

## Fixes Applied

### 1. **Capture Baseline at the Right Time** ✅

**File:** `ui/calibration_dialog.py`

Now captures baseline in `_enable_button_detection()` - exactly when "Ready!" appears:

```python
def _enable_button_detection(self):
    # Capture baseline NOW (when user is NOT pressing anything)
    data = self.hid_device.read(64)
    if data:
        self.logic.baseline_data = bytes(data)
        self.log(f"Baseline captured: [{hex_str}...]")  # Debug

    self.detection_enabled = True
```

**Timeline:**
1. Instruction appears: "Press button A (Ready in 1 second...) Release all buttons!"
2. User has 1 second to release any pressed buttons
3. After 1 second: Baseline captured
4. Then: "✓ Ready! Press the button now."
5. User presses button
6. Change detected!

### 2. **Reduced Detection Threshold** ✅

**File:** `ui/calibration_logic.py`

Changed from 3 to 1:
```python
# Before:
if diff >= 3:  # Too high!

# After:
if diff >= 1:  # Correct for buttons
```

Now detects:
- `0x00` → `0x01` ✓
- `0x00` → `0x02` ✓
- Any single bit change ✓

### 3. **Exclude Mapped Axes** ✅

**Files:**
- `ui/calibration_dialog.py`
- `ui/calibration_logic.py`

Pass all mapped axes to exclude them:
```python
# In dialog:
mapped_byte_indices = {cfg['offset'] for cfg in self.mapped_axes.values()}
result = self.logic.detect_button(data, self.axes_config, mapped_byte_indices)

# In logic:
def detect_button(self, raw_data, axes_config, mapped_axes=None):
    axes_to_ignore = set(self.detected_axes)
    if mapped_axes:
        axes_to_ignore.update(mapped_axes)  # Ignore these too!
```

This prevents:
- Axis jitter being detected as button press
- Confusion when stick moves during button press

### 4. **Added Debug Logging** ✅

**File:** `ui/calibration_dialog.py`

Now shows in Activity Log:
```
Baseline captured: [01 00 00 f0 00 80 14 81...]
Multiple changes (3): byte 2=01, byte 5=81, byte 7=ff
✓ Mapped A -> Byte 2 = 01
```

This helps you see:
- When baseline is captured
- What changes are detected
- Why detection might not work (multiple changes)

---

## How It Works Now

### Button Detection Flow:

1. **Instruction Phase (1 second)**
   ```
   "Press button: A"
   "(Ready in 1 second...)"
   "Release all buttons!"
   ```
   - Detection: DISABLED
   - User releases any pressed buttons

2. **Baseline Capture**
   ```
   [After 1 second]
   Baseline captured: [01 00 00 f0 ...]
   ```
   - Baseline saved with NO buttons pressed

3. **Ready Phase**
   ```
   "Press button: A"
   "✓ Ready! Press the button now."
   ```
   - Detection: ENABLED
   - Waiting for button press

4. **Detection**
   ```
   User presses button
   Byte 2 changes: 0x00 → 0x01 (diff = 1)
   ✓ Detected!
   "✓ Mapped A -> Byte 2 = 01"
   ```
   - Single byte changed
   - Detection successful!

5. **Advance**
   - Detection: DISABLED
   - Cooldown: 500ms
   - Next button instruction

---

## Debug Information

When testing, watch the Activity Log for:

### Success:
```
Baseline captured: [01 00 00 f0 00 80 14 81...]
✓ Mapped A -> Byte 2 = 01
```

### Multiple Changes (waiting):
```
Multiple changes (3): byte 2=01, byte 5=81, byte 7=ff
```
This means multiple bytes changed - probably axis movement or noise.
Press ONLY the button without moving sticks!

### No Detection:
- Check if baseline was captured (should show in log)
- Try pressing button harder
- Try different button
- Click "Skip" and try next button

---

## Testing

```bash
python3 main.py
# Click "Auto-Calibrate"
# Complete axis calibration
# Watch Activity Log during button mapping:
#   - Should see "Baseline captured"
#   - Should see "Multiple changes" if you move sticks
#   - Should see "✓ Mapped X" when you press correctly
```

**Tips:**
- Don't move sticks during button mapping!
- Press buttons clearly and deliberately
- Wait for "✓ Ready!" before pressing
- Watch Activity Log for debug info

---

## Summary

**Before:**
- Baseline wrong timing → no detection
- Threshold too high → missed simple buttons
- Axes interfering → false positives/negatives
- No debug info → blind troubleshooting

**After:**
- ✅ Baseline captured at perfect time (after "ready" delay)
- ✅ Threshold = 1 (detects all buttons)
- ✅ Mapped axes excluded (no interference)
- ✅ Debug logging (see what's happening)

**Result:** Button detection should work now! 🎮
