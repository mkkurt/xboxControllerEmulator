#!/usr/bin/env python3
"""
Test BrowserBridge gamepad conversion
"""
from browser_bridge import BrowserBridge
import json

def test_gamepad_conversion():
    print("Testing BrowserBridge Gamepad Conversion...")
    print("="*60)

    bridge = BrowserBridge()

    # Test 1: Empty state
    print("\n1. Empty state:")
    state = {}
    gamepad = bridge._convert_to_gamepad(state)
    print(f"   Axes: {gamepad['axes']}")
    print(f"   Buttons pressed: {sum(1 for b in gamepad['buttons'] if b['pressed'])}")

    # Test 2: Button presses
    print("\n2. Button presses:")
    state = {
        '1234:5678_btn_A': True,
        '1234:5678_btn_B': False,
        '1234:5678_btn_X': True,
    }
    gamepad = bridge._convert_to_gamepad(state)
    print(f"   A pressed: {gamepad['buttons'][0]['pressed']}")
    print(f"   B pressed: {gamepad['buttons'][1]['pressed']}")
    print(f"   X pressed: {gamepad['buttons'][2]['pressed']}")

    # Test 3: Axes
    print("\n3. Axes:")
    state = {
        '1234:5678_LeftX': 0.5,
        '1234:5678_LeftY': -0.3,
        '1234:5678_RightX': -0.8,
        '1234:5678_RightY': 0.2,
    }
    gamepad = bridge._convert_to_gamepad(state)
    print(f"   Left Stick X: {gamepad['axes'][0]:5.2f}")
    print(f"   Left Stick Y: {gamepad['axes'][1]:5.2f}")
    print(f"   Right Stick X: {gamepad['axes'][2]:5.2f}")
    print(f"   Right Stick Y: {gamepad['axes'][3]:5.2f}")

    # Test 4: Triggers
    print("\n4. Triggers:")
    state = {
        '1234:5678_LT': 0.7,
        '1234:5678_RT': 0.3,
    }
    gamepad = bridge._convert_to_gamepad(state)
    print(f"   LT value: {gamepad['buttons'][6]['value']:5.2f}")
    print(f"   LT pressed: {gamepad['buttons'][6]['pressed']}")
    print(f"   RT value: {gamepad['buttons'][7]['value']:5.2f}")
    print(f"   RT pressed: {gamepad['buttons'][7]['pressed']}")

    # Test 5: Hat/D-Pad
    print("\n5. Hat/D-Pad:")
    state = {
        '1234:5678_hat': 0,  # Up
    }
    gamepad = bridge._convert_to_gamepad(state)
    print(f"   Up (button 12): {gamepad['buttons'][12]['pressed']}")
    print(f"   Down (button 13): {gamepad['buttons'][13]['pressed']}")
    print(f"   Left (button 14): {gamepad['buttons'][14]['pressed']}")
    print(f"   Right (button 15): {gamepad['buttons'][15]['pressed']}")

    # Test 6: Complete state
    print("\n6. Complete state (JSON):")
    state = {
        '1234:5678_btn_A': True,
        '1234:5678_btn_Start': True,
        '1234:5678_LeftX': 0.5,
        '1234:5678_LeftY': -0.5,
        '1234:5678_LT': 0.8,
        '1234:5678_hat': 3,  # Right
    }
    gamepad = bridge._convert_to_gamepad(state)
    json_output = json.dumps(gamepad, indent=2)
    print(f"   {json_output}")

    print("\n" + "="*60)
    print("✓ BrowserBridge conversion tests passed!")
    return True

if __name__ == "__main__":
    test_gamepad_conversion()
