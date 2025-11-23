#!/usr/bin/env python3
"""
Test DSU Server basic functionality
"""
from dsu_server import DSUServer
import time

def test_dsu_server():
    print("Testing DSU Server...")
    print("="*60)

    # Test 1: Instantiation
    print("\n1. Creating DSU Server instance...")
    try:
        server = DSUServer(port=26761)  # Use different port to avoid conflicts
        print("   ✓ DSU Server created successfully")
    except Exception as e:
        print(f"   ✗ Failed to create server: {e}")
        return False

    # Test 2: State update
    print("\n2. Testing state update...")
    test_state = {
        'buttons': 0x01,  # A button
        'joy_x': 0.5,
        'joy_y': -0.3,
        'hat': 0
    }
    try:
        server.update(test_state)
        print("   ✓ State updated successfully")
        print(f"   State: {server.state}")
    except Exception as e:
        print(f"   ✗ Failed to update state: {e}")
        return False

    # Test 3: Start server (briefly)
    print("\n3. Testing server start/stop...")
    try:
        server.start()
        print("   ✓ Server started")
        time.sleep(0.5)
        server.stop()
        print("   ✓ Server stopped")
    except Exception as e:
        print(f"   ✗ Server start/stop failed: {e}")
        return False

    print("\n" + "="*60)
    print("✓ DSU Server basic tests passed!")
    print("\nNote: Full DSU protocol testing requires a DSU client.")
    return True

if __name__ == "__main__":
    test_dsu_server()
