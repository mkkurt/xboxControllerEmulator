"""
Input Processor - Advanced Input Manipulation
Handles deadzones, response curves, and smoothing for controller axes.
"""
import math

class InputProcessor:
    def __init__(self):
        # Configuration defaults
        self.config = {
            'deadzone': 0.05,      # 5% deadzone
            'curve': 1.0,          # 1.0 = Linear, >1.0 = Exponential (finer center)
            'smoothing': 0.0,      # 0.0 = No smoothing, 1.0 = Max smoothing (unresponsive)
            'deadzone_mode': 'axial' # 'axial' or 'radial' (radial requires X/Y pairs)
        }
        
        # State for smoothing
        self.last_values = {}  # axis_name -> value
    
    def update_config(self, new_config):
        """Update processing configuration"""
        self.config.update(new_config)

    def process_axis(self, axis_name, value, dt=0.016):
        """
        Process a single axis value (-1.0 to 1.0)
        Returns processed value
        """
        # 1. Apply Deadzone
        value = self._apply_deadzone(value)
        
        # 2. Apply Response Curve
        value = self._apply_curve(value)
        
        # 3. Apply Smoothing
        value = self._apply_smoothing(axis_name, value, dt)
        
        return value

    def _apply_deadzone(self, value):
        """Apply axial deadzone and rescale remaining range"""
        dz = self.config['deadzone']
        if abs(value) < dz:
            return 0.0
        
        # Rescale the remaining range 0..1 to start after deadzone
        # This prevents a "jump" in output when leaving the deadzone
        sign = 1.0 if value > 0 else -1.0
        normalized = (abs(value) - dz) / (1.0 - dz)
        return sign * normalized

    def _apply_curve(self, value):
        """Apply exponential response curve"""
        curve = self.config['curve']
        if curve == 1.0:
            return value
        
        # Apply curve: output = input^curve (preserving sign)
        # curve > 1 makes center less sensitive (precision)
        # curve < 1 makes center more sensitive (aggressive)
        sign = 1.0 if value > 0 else -1.0
        return sign * (abs(value) ** curve)

    def _apply_smoothing(self, axis_name, value, dt):
        """Apply Exponential Moving Average (EMA) smoothing"""
        smoothing = self.config['smoothing']
        if smoothing <= 0.0:
            return value
            
        # Calculate alpha based on smoothing factor and delta time
        # smoothing 0.0 -> alpha 1.0 (instant)
        # smoothing 0.9 -> alpha small (slow)
        # We map 0..1 smoothing to a time constant
        
        if axis_name not in self.last_values:
            self.last_values[axis_name] = value
            return value
            
        last_val = self.last_values[axis_name]
        
        # Simple EMA: new = alpha * current + (1-alpha) * last
        # Map config smoothing (0-1) to alpha (1-0)
        alpha = 1.0 - min(0.95, smoothing)
        
        new_val = alpha * value + (1.0 - alpha) * last_val
        self.last_values[axis_name] = new_val
        
        return new_val
