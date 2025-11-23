import unittest
from ui.calibration_logic import CalibrationLogic

class TestCalibrationLogic(unittest.TestCase):
    def setUp(self):
        self.logic = CalibrationLogic()

    def test_axis_detection(self):
        # Simulate axis movement on byte 0
        # Baseline
        self.logic.process_axis_calibration([128, 0, 0])
        
        # Move min
        self.logic.process_axis_calibration([0, 0, 0])
        
        # Move max
        self.logic.process_axis_calibration([255, 0, 0])
        
        # Finalize
        axes = self.logic.finalize_axes()
        
        self.assertIn(0, axes)
        self.assertEqual(axes[0]['min'], 0)
        self.assertEqual(axes[0]['max'], 255)
        self.assertEqual(axes[0]['center'], 128)
        
        # Byte 1 didn't move
        self.assertNotIn(1, axes)

    def test_axis_mapping_detection(self):
        # Setup known axes
        axes_config = {
            0: {'min': 0, 'max': 255, 'center': 128},
            1: {'min': 0, 'max': 255, 'center': 128}
        }
        
        # Test movement detection
        # Center
        result = self.logic.detect_axis_movement([128, 128], axes_config)
        self.assertIsNone(result)
        
        # Small movement (noise)
        result = self.logic.detect_axis_movement([130, 128], axes_config)
        self.assertIsNone(result)
        
        # Large movement on one axis
        result = self.logic.detect_axis_movement([250, 128], axes_config)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 0) # Byte 0
        self.assertEqual(result[1], 250) # Value
        
        # Movement on both axes, but one is stronger
        # Byte 0: 250 (strong), Byte 1: 150 (weak)
        result = self.logic.detect_axis_movement([250, 150], axes_config)
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 0) # Should pick stronger one

    def test_button_detection(self):
        # Setup: Byte 0 is an axis, Byte 1 is buttons
        self.logic.detected_axes.add(0)
        self.logic.baseline_data = bytes([128, 0])
        
        # Test button press on Byte 1
        # 0 -> 1
        result = self.logic.detect_button([128, 1], {})
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 1)
        self.assertEqual(result[1], 1)
        
        # Test axis movement (should be ignored)
        result = self.logic.detect_button([200, 0], {})
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
