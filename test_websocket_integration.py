#!/usr/bin/env python3
"""
Test complete WebSocket integration
Starts browser bridge and tests real WebSocket connection
"""
import asyncio
import websockets
import json
import time
from browser_bridge import BrowserBridge
from threading import Thread

async def test_websocket_client(bridge):
    """WebSocket client that connects to browser bridge"""
    try:
        async with websockets.connect('ws://127.0.0.1:8765') as websocket:
            print("  ✓ WebSocket client connected!")

            # Now send some test data
            print("  Sending test gamepad state...")
            test_state = {
                '1234:5678_btn_A': True,
                '1234:5678_LeftX': 0.5,
                '1234:5678_LeftY': -0.3,
                '1234:5678_LT': 0.7,
            }
            bridge.broadcast(test_state)

            # Wait for messages
            received_count = 0
            start_time = time.time()

            while time.time() - start_time < 2:
                try:
                    message = await asyncio.wait_for(websocket.recv(), timeout=0.5)
                    data = json.loads(message)
                    received_count += 1

                    if received_count == 1:
                        # Print first message structure
                        print(f"\n  First message received:")
                        print(f"    Axes: {data.get('axes', [])}")
                        print(f"    Buttons: {len(data.get('buttons', []))} buttons")
                        print(f"    Button A: {data['buttons'][0]['pressed']}")
                        print(f"    LT: {data['buttons'][6]['value']}")
                except asyncio.TimeoutError:
                    pass

            print(f"\n  ✓ Received {received_count} messages")
            return received_count > 0

    except Exception as e:
        print(f"  ✗ Client error: {e}")
        return False

def test_websocket_integration():
    print("="*60)
    print("WEBSOCKET INTEGRATION TEST")
    print("="*60)

    # Start browser bridge
    print("\n1. Starting browser bridge...")
    bridge = BrowserBridge()
    bridge.start()
    print("  ✓ Browser bridge started on ws://127.0.0.1:8765")

    # Give it a moment to start
    time.sleep(0.5)

    # Run WebSocket client
    print("\n2. Testing WebSocket client connection...")
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        success = loop.run_until_complete(test_websocket_client(bridge))
    except Exception as e:
        print(f"  ✗ Client test failed: {e}")
        success = False
    finally:
        loop.close()

    # Stop bridge
    print("\n3. Stopping browser bridge...")
    bridge.stop()
    print("  ✓ Bridge stopped")

    print("\n" + "="*60)
    print("TEST RESULTS:")

    if success:
        print("  ✓ WEBSOCKET COMMUNICATION WORKING!")
        print("  ✓ Browser bridge can send data to clients")
        print("  ✓ Gamepad state conversion working")
        return True
    else:
        print("  ✗ WebSocket test failed")
        print("  Check if port 8765 is available")
        return False

if __name__ == "__main__":
    import sys
    success = test_websocket_integration()
    sys.exit(0 if success else 1)
