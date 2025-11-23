#!/usr/bin/env python3
"""
Test script to verify inputs library detection works with user's devices
"""
from inputs import get_gamepad, devices
import sys

def main():
    print("="*60)
    print("INPUTS LIBRARY DEVICE DETECTION TEST")
    print("="*60)
    
    # List all detected devices
    print("\nDetected devices:")
    if not devices.gamepads:
        print("  No gamepads/joysticks detected!")
        return 1
    
    for i, device in enumerate(devices.gamepads):
        print(f"\nDevice {i}: {device}")
        print(f"  Name: {device.name}")
        print(f"  Path: {device._device_path}")
    
    print("\n" + "="*60)
    print("Testing live input... (Press Ctrl+C to stop)")
    print("="*60)
    
    try:
        while True:
            events = get_gamepad()
            for event in events:
                print(f"{event.ev_type} {event.code}: {event.state}")
    except KeyboardInterrupt:
        print("\n\nTest completed successfully!")
    except Exception as e:
        print(f"\nError: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
