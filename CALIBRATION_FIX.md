# Calibration Wizard Fix - Auto-Advancing Bug

## Problem

The calibration wizard was automatically skipping through steps without waiting for user input:
- Would rapidly cycle through all axes in sequence
- Would auto-map buttons without user pressing them deliberately
- Appeared to be applying detected input to all steps automatically

**Root Cause:** The wizard was continuously detecting input with no delays or debouncing. Any residual movement or noise from previous steps would trigger detection for the next step immediately.

---

## What Was Fixed

### 1. **Added Detection Enable/Disable Flag**

**File:** `ui/calibration_dialog.py`

Added `detection_enabled` flag that controls whether input detection is active:
```python
self.detection_enabled = False  # Only detect when ready
```

Detection is now:
- **DISABLED** when showing a new instruction
- **ENABLED** after a 1-second delay
- **DISABLED** immediately after detecting an input

This prevents:
- Detecting residual movement from previous calibration
- Auto-skipping through steps
- Detecting noise as intentional input

---

### 2. **Added 1-Second Preparation Delay**

**File:** `ui/calibration_dialog.py`

When a new axis/button instruction appears:
```python
self.instruction_label.setText(f"Move/Press: {axis_name}\n\n(Ready in 1 second...)")
QTimer.singleShot(1000, self._enable_axis_detection)
```

After 1 second:
```python
self.instruction_label.setText(f"Move/Press: {axis_name}\n\n✓ Ready! Move the axis now.")
self.detection_enabled = True
```

**User Experience:**
- User sees what to do
- Has 1 second to prepare
- Clear visual feedback when ready ("✓ Ready!")
- No accidental detections during transition

---

### 3. **Added Cooldown Period Between Detections**

**File:** `ui/calibration_dialog.py`

Added 500ms cooldown to prevent detecting same input multiple times:
```python
self.detection_cooldown = 0.5  # Minimum 500ms between detections
self.last_detection_time = 0

# In detection code:
current_time = time.time()
if current_time - self.last_detection_time < self.detection_cooldown:
    return  # Skip detection
```

This prevents:
- Detecting the same axis movement multiple times
- Rapid auto-advancement
- Bounce/chatter from mechanical switches

---

### 4. **Reset Baseline Between Steps**

**File:** `ui/calibration_dialog.py`

Before each new detection, reset the baseline:
```python
self.logic.baseline_data = None
```

This ensures:
- Each step starts fresh
- Previous movements don't affect current detection
- Cleaner signal-to-noise ratio

---

### 5. **Increased Detection Thresholds**

**File:** `ui/calibration_logic.py`

**Axis Movement:**
- Old: 15% deviation required
- New: **30% deviation required**

```python
# Require 30% deviation to avoid noise (increased from 15%)
if percent_deviation > 0.30:
```

**Button Press:**
- Old: Any change (diff > 0)
- New: **Minimum 3 units of change**

```python
# Require at least 3 units of change to avoid noise
if diff >= 3:
```

This prevents:
- Noise from being detected as input
- Small axis drift triggering detection
- Bit flips being interpreted as button presses

---

## How It Works Now

### Axis Mapping Flow:

1. **Instruction appears:** "Move/Press: Left Stick X (Ready in 1 second...)"
   - Detection DISABLED
   - Baseline reset
   - Timer started

2. **After 1 second:** "Move/Press: Left Stick X ✓ Ready! Move the axis now."
   - Detection ENABLED
   - User can now move axis

3. **User moves axis significantly (>30%)**
   - Axis detected
   - Logged: "✓ Mapped Left Stick X -> Byte 5"
   - Detection DISABLED immediately
   - Cooldown timer started

4. **Advance to next axis**
   - Go back to step 1 for next axis

### Button Mapping Flow:

Same pattern:
1. Show instruction with countdown
2. Enable detection after delay
3. Wait for significant button press (diff >= 3)
4. Detect, log, disable, advance

---

## Testing

**Before Fix:**
```
User: Starts calibration
Wizard: "Move Left Stick X"
Wizard: *immediately* "Move Left Stick Y"
Wizard: *immediately* "Move Right Stick X"
Wizard: *immediately* "Move Right Stick Y"
Result: All axes auto-mapped incorrectly!
```

**After Fix:**
```
User: Starts calibration
Wizard: "Move Left Stick X (Ready in 1 second...)"
[1 second pause]
Wizard: "Move Left Stick X ✓ Ready! Move the axis now."
User: Moves left stick X
Wizard: "✓ Mapped Left Stick X -> Byte 5"
[500ms cooldown]
Wizard: "Move Left Stick Y (Ready in 1 second...)"
[1 second pause]
Wizard: "Move Left Stick Y ✓ Ready! Move the axis now."
User: Moves left stick Y
Result: Correct mapping!
```

---

## Files Modified

1. **ui/calibration_dialog.py**
   - Added `detection_enabled` flag
   - Added `last_detection_time` and cooldown
   - Added preparation delays (1 second)
   - Added `_enable_axis_detection()` and `_enable_button_detection()`
   - Modified `process_input()` to check flags
   - Modified `on_axis_detected()` and `on_button_detected()` to disable detection

2. **ui/calibration_logic.py**
   - Increased axis detection threshold: 15% → 30%
   - Increased button detection threshold: 0 → 3 units

---

## User Experience Improvements

✅ **No more auto-skipping** - User has full control
✅ **Clear feedback** - Shows "Ready in 1 second" then "✓ Ready!"
✅ **Deliberate actions** - Requires significant movement (30%)
✅ **No accidental detections** - Cooldown prevents bouncing
✅ **Reliable mapping** - Each step is independent

---

## Testing Instructions

```bash
# Launch the app
python3 main.py

# Click "Auto-Calibrate"
# You should now see:
# 1. "Ready in 1 second..." message
# 2. Then "✓ Ready! Move the axis now."
# 3. Each step waits for YOUR input
# 4. No auto-skipping!
```

Expected behavior:
- Wizard waits for you at each step
- You have time to read instructions
- Clear "Ready" indicator before detection starts
- Only advances when you deliberately move/press

---

## Summary

**Root Cause:** Continuous detection with no delays or thresholds
**Solution:** Added enable/disable control, delays, cooldowns, and higher thresholds
**Result:** Calibration wizard now waits for deliberate user input at each step

The wizard is now **user-controlled** instead of auto-advancing! 🎉
