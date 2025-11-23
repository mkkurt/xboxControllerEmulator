
import unittest
import random
from ui.calibration_logic import CalibrationLogic

class TestCalibrationRobustness(unittest.TestCase):
    def setUp(self):
        self.logic = CalibrationLogic()

    def test_noise_rejection_step0(self):
        """Test that small noise (Range < 80) is not detected as an axis in Step 0"""

        # Simulate noise (Range 30)
        # Center 128, +/- 15
        for _ in range(100):
            val = 128 + random.randint(-15, 15)
            data = [0] * 64
            data[0] = val
            self.logic.process_axis_calibration(data)

        axes_config = self.logic.finalize_axes()

        # Should NOT be in axes_config because threshold is 80
        self.assertNotIn(0, axes_config, "Noise (Range 30) should not be detected as an axis")

        # Should be in noisy_axes because Range > 5
        self.assertIn(0, self.logic.noisy_axes, "Noise (Range 30) should be marked as noisy")

    def test_noise_rejection_step1(self):
        """Test that noise on a valid axis does not trigger detection in Step 1"""

        # First, force an axis to be detected (Simulate Range 100)
        for _ in range(100):
            val = random.randint(50, 150) # Range 100
            data = [0] * 64
            data[0] = val
            self.logic.process_axis_calibration(data)

        axes_config = self.logic.finalize_axes()
        self.assertIn(0, axes_config)
        center = axes_config[0]['center']

        # Now simulate idle noise (deviation < 20 or < 30%)
        # Center is approx 100. Range is 100.
        # Deviation > 20 is required AND > 30% (30 units).
        # Let's try deviation 25. (25 > 20, but 25/100 = 25% < 30%) -> Should NOT trigger.

        val = center + 25
        # Clamp to min/max
        val = max(axes_config[0]['min'], min(axes_config[0]['max'], val))

        data = [0] * 64
        data[0] = val

        result = self.logic.detect_axis_movement(data, axes_config)
        self.assertIsNone(result, f"Deviation 25 on Range 100 (25%) should not trigger. Val={val}, Center={center}")

    def test_valid_movement_step1(self):
        """Test that valid large movement triggers detection in Step 1"""

        # Setup valid axis
        for _ in range(100):
            val = random.randint(0, 255) # Range 255
            data = [0] * 64
            data[0] = val
            self.logic.process_axis_calibration(data)

        axes_config = self.logic.finalize_axes()
        self.assertIn(0, axes_config)

        # Move to max (approx 128 deviation)
        val = 255
        data = [0] * 64
        data[0] = val

        result = self.logic.detect_axis_movement(data, axes_config)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 0)

    def test_noisy_axis_ignored_in_buttons(self):
        """Test that an axis rejected in Step 0 (because noisy) is ignored in Step 2 (Buttons)"""

        # Simulate Noisy Axis (Range 40) -> Should be rejected as axis but marked noisy
        for _ in range(100):
            val = 128 + random.randint(-20, 20)
            data = [0] * 64
            data[0] = val
            self.logic.process_axis_calibration(data)

        axes_config = self.logic.finalize_axes()
        self.assertNotIn(0, axes_config)
        self.assertIn(0, self.logic.noisy_axes)

        # Now simulate Step 2 (Button Detection)
        # Establish baseline
        self.logic.baseline_data = bytes([128] * 64)

        # Change the noisy axis by 10 units (significant for button, but it's a noisy axis)
        data = [128] * 64
        data[0] = 138

        result = self.logic.detect_button(data, axes_config)
        self.assertIsNone(result, "Should ignore movement on noisy axis when detecting buttons")

    def test_real_button_detection(self):
        """Test that a real button press (stable byte 0->1) is detected"""

        # Step 0: Ensure byte 1 is STABLE (Range 0)
        for _ in range(100):
            data = [0] * 64 # All 0
            self.logic.process_axis_calibration(data)

        axes_config = self.logic.finalize_axes()
        self.assertNotIn(1, axes_config)
        self.assertNotIn(1, self.logic.noisy_axes)

        # Step 2: Button Detection
        self.logic.baseline_data = bytes([0] * 64)

        # Press button on byte 1
        data = [0] * 64
        data[1] = 1 # 0 -> 1

        result = self.logic.detect_button(data, axes_config)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 1)

if __name__ == '__main__':
    unittest.main()
