import math

class CalibrationLogic:
    """
    Handles the logic for controller calibration:
    1. Axis detection and range calibration
    2. Button detection
    3. Deadzone calculation
    """
    def __init__(self):
        self.reset()
        
    def reset(self):
        # Axis calibration data
        # Map of byte_index -> {min, max, center, samples}
        self.axis_data = {}
        
        # Detected axes: list of byte indices that are confirmed as axes
        self.detected_axes = set()
        
        # Baseline data for noise filtering
        self.baseline_data = None
        
        # Button mappings: name -> byte_index
        self.button_mappings = {}
        
    def process_axis_calibration(self, raw_data):
        """
        Process raw data during axis calibration stage.
        Updates min/max/center for potential axes.
        """
        data = bytes(raw_data)
        
        if self.baseline_data is None:
            self.baseline_data = data
            # Also initialize axis data with this baseline to capture initial center
            for i, value in enumerate(data):
                self.axis_data[i] = {
                    'min': value,
                    'max': value,
                    'center': value,
                    'samples': [value]
                }
            return
            
        for i, value in enumerate(data):
            if i not in self.axis_data:
                self.axis_data[i] = {
                    'min': value,
                    'max': value,
                    'center': value, # Assumes starting position is center (roughly)
                    'samples': [value]
                }
            else:
                stats = self.axis_data[i]
                stats['min'] = min(stats['min'], value)
                stats['max'] = max(stats['max'], value)
                stats['samples'].append(value)
                
                # Keep sample size manageable
                if len(stats['samples']) > 100:
                    stats['samples'].pop(0)

    def finalize_axes(self):
        """
        Analyze collected data to determine which bytes are actually axes.
        Returns a dictionary of axis configurations.
        """
        final_axes = {}
        
        for i, stats in self.axis_data.items():
            total_range = stats['max'] - stats['min']
            
            # Threshold to consider something an axis
            # A real axis should move significantly (e.g. > 20 values in 0-255 range)
            if total_range > 20:
                self.detected_axes.add(i)
                
                # Calculate center more accurately if possible
                # For now, we'll assume the initial value was roughly center
                # or the average of min/max if it looks like a full range axis
                center = stats['center']
                
                # Calculate deadzone based on noise at center
                # This is a simplification; a real implementation might track center jitter separately
                deadzone = 0.05 # Default 5%
                
                final_axes[i] = {
                    'min': stats['min'],
                    'max': stats['max'],
                    'center': center,
                    'deadzone': deadzone
                }
                
        return final_axes

    def detect_button(self, raw_data, axes_config, mapped_axes=None):
        """
        Detect if a button is pressed, ignoring known axes.
        Returns (byte_index, value) or None.
        """
        data = bytes(raw_data)

        if self.baseline_data is None:
            self.baseline_data = data
            return None

        # Combine all axes to ignore
        axes_to_ignore = set(self.detected_axes)
        if mapped_axes:
            axes_to_ignore.update(mapped_axes)

        # Check for changes
        candidates = []

        for i, (base, current) in enumerate(zip(self.baseline_data, data)):
            # Skip known axes and mapped axes
            if i in axes_to_ignore:
                continue

            diff = abs(int(current) - int(base))

            # Require at least 1 unit of change to detect button press
            # Buttons can be simple on/off (0x00 -> 0x01)
            if diff >= 1:
                candidates.append((i, current, diff))  # Store diff for filtering

        # Store for debugging
        self.last_candidates_count = len(candidates)
        self.last_candidates = [(i, val) for i, val, _ in candidates]  # Store without diff for compatibility

        # If exactly one change, it's definitely our button
        if len(candidates) == 1:
            return (candidates[0][0], candidates[0][1])

        # If multiple changes detected, filter out small changes (likely noise/coupled axes)
        if len(candidates) > 1:
            # Filter out small changes (< 10 units)
            # These are likely analog axes with minor jitter or coupled movement
            significant_changes = [c for c in candidates if c[2] >= 10]

            # If we filtered down to exactly one significant change, that's our button
            if len(significant_changes) == 1:
                self.last_filter_reason = f"Filtered {len(candidates)} changes to 1 significant (>= 10 units)"
                return (significant_changes[0][0], significant_changes[0][1])

            # If multiple significant changes remain, pick the largest
            # This handles cases where a button press causes multiple related bytes to change
            if len(significant_changes) > 1:
                largest = max(significant_changes, key=lambda x: x[2])
                self.last_filter_reason = f"Selected largest of {len(significant_changes)} significant changes (diff={largest[2]})"
                return (largest[0], largest[1])

            # All changes were small (< 10), might be noise or need lower threshold
            # In this case, still pick the largest change
            if candidates:
                largest = max(candidates, key=lambda x: x[2])
                if largest[2] >= 3:  # At least 3 units of change
                    self.last_filter_reason = f"All changes small, picked largest (diff={largest[2]})"
                    return (largest[0], largest[1])

        return None

    def detect_axis_movement(self, raw_data, axes_config, excluded_axes=None):
        """
        Detect which axis is being moved significantly.
        Returns (byte_index, value) or None.
        """
        data = bytes(raw_data)
        excluded = excluded_axes or set()
        
        best_candidate = None
        max_deviation = 0.0
        
        for i, config in axes_config.items():
            if i in excluded:
                continue
                
            current_val = data[i]
            center = config['center']
            min_val = config['min']
            max_val = config['max']
            
            # Range of this axis
            total_range = max_val - min_val
            if total_range == 0: continue
            
            deviation = abs(current_val - center)
            percent_deviation = deviation / total_range

            # Require 30% deviation to avoid noise (increased from 15%)
            if percent_deviation > 0.30:
                if percent_deviation > max_deviation:
                    max_deviation = percent_deviation
                    best_candidate = (i, current_val)
        
        return best_candidate
