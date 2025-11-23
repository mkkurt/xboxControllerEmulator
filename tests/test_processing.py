"""
Test script for InputProcessor logic
Verifies deadzones, curves, and smoothing math.
"""
import unittest
from input_processor import InputProcessor

class TestInputProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = InputProcessor()
        
    def test_deadzone_axial(self):
        """Test axial deadzone logic"""
        self.processor.update_config({'deadzone': 0.1, 'curve': 1.0, 'smoothing': 0.0})
        
        # Inside deadzone -> 0
        self.assertEqual(self.processor.process_axis('x', 0.05), 0.0)
        self.assertEqual(self.processor.process_axis('x', -0.05), 0.0)
        
        # Outside deadzone -> Scaled 0..1
        # 0.1 is boundary (0), 1.0 is max (1)
        # Input 0.55 (midpoint of 0.1-1.0) should be 0.5
        self.assertAlmostEqual(self.processor.process_axis('x', 0.55), 0.5)
        self.assertAlmostEqual(self.processor.process_axis('x', 1.0), 1.0)
        
    def test_response_curve(self):
        """Test exponential response curve"""
        # Curve 2.0 (Quadratic)
        self.processor.update_config({'deadzone': 0.0, 'curve': 2.0, 'smoothing': 0.0})
        
        # 0.5 input -> 0.25 output
        self.assertAlmostEqual(self.processor.process_axis('x', 0.5), 0.25)
        self.assertAlmostEqual(self.processor.process_axis('x', -0.5), -0.25)
        self.assertAlmostEqual(self.processor.process_axis('x', 1.0), 1.0)
        
    def test_smoothing(self):
        """Test EMA smoothing"""
        # Smoothing 0.5 -> Alpha ~0.5
        self.processor.update_config({'deadzone': 0.0, 'curve': 1.0, 'smoothing': 0.5})
        
        # First value sets baseline
        val1 = self.processor.process_axis('x', 1.0)
        self.assertEqual(val1, 1.0)
        
        # Jump to 0.0
        # New = 0.5 * 0.0 + 0.5 * 1.0 = 0.5
        val2 = self.processor.process_axis('x', 0.0)
        self.assertAlmostEqual(val2, 0.5)
        
        # Stay at 0.0
        # New = 0.5 * 0.0 + 0.5 * 0.5 = 0.25
        val3 = self.processor.process_axis('x', 0.0)
        self.assertAlmostEqual(val3, 0.25)

if __name__ == '__main__':
    unittest.main()
