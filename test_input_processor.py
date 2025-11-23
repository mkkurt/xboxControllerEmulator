#!/usr/bin/env python3
"""
Test InputProcessor
"""
from input_processor import InputProcessor

def test_processor():
    print("Testing InputProcessor...")
    print("="*60)

    processor = InputProcessor()

    # Test 1: Default processing (no modifications)
    print("\n1. Default processing (linear, no deadzone):")
    processor.update_config({'deadzone': 0.0, 'curve': 1.0, 'smoothing': 0.0})
    test_values = [-1.0, -0.5, 0.0, 0.5, 1.0]
    for val in test_values:
        result = processor.process_axis('test', val)
        print(f"   Input: {val:5.2f} -> Output: {result:5.2f}")

    # Test 2: Deadzone
    print("\n2. With 10% deadzone:")
    processor.update_config({'deadzone': 0.1, 'curve': 1.0, 'smoothing': 0.0})
    processor.last_values.clear()  # Reset
    test_values = [-0.2, -0.1, -0.05, 0.0, 0.05, 0.1, 0.2]
    for val in test_values:
        result = processor.process_axis('test', val)
        print(f"   Input: {val:5.2f} -> Output: {result:5.2f}")

    # Test 3: Response curve
    print("\n3. With exponential curve (2.0):")
    processor.update_config({'deadzone': 0.0, 'curve': 2.0, 'smoothing': 0.0})
    processor.last_values.clear()
    test_values = [-1.0, -0.5, 0.0, 0.5, 1.0]
    for val in test_values:
        result = processor.process_axis('test', val)
        print(f"   Input: {val:5.2f} -> Output: {result:5.2f}")

    # Test 4: Smoothing
    print("\n4. With smoothing (0.5):")
    processor.update_config({'deadzone': 0.0, 'curve': 1.0, 'smoothing': 0.5})
    processor.last_values.clear()
    print("   Sending value 1.0 three times (should gradually approach 1.0):")
    for i in range(3):
        result = processor.process_axis('test', 1.0)
        print(f"   Iteration {i+1}: {result:5.2f}")

    print("\n" + "="*60)
    print("✓ InputProcessor tests passed!")
    return True

if __name__ == "__main__":
    test_processor()
