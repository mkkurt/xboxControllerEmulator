import asyncio
import websockets
import json
import threading

class BrowserBridge:
    def __init__(self, port=8765):
        self.port = port
        self.clients = set()
        self.loop = None
        self.thread = None
        self.running = False

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_server)
        self.thread.start()

    def stop(self):
        self.running = False
        # In a real app we'd signal the loop to stop, but for this simple script
        # we'll just let the daemon thread die or rely on main exit.
        pass

    def broadcast(self, state):
        if not self.clients:
            return
        
        # Convert state to standard Gamepad API format
        # Mapping for MSFS 2024 (Xbox Controller Layout)
        # Left Stick: Joystick X/Y (Pitch/Roll)
        # Right Stick: Throttle (mapped to Y axis?) or Camera. 
        # Let's map Throttle to Triggers (LT/RT) for analog control.
        # D-Pad: Hat Switch (POV 1)
        # A: Trigger (Button 1) - Select / Fire
        # B: Weapon Release (Button 2 - Red Button) - Back / Cancel
        # X: Pinky Switch (Button 3) - Context 1
        # Y: Paddle Switch (Button 4) - Context 2
        
        buttons_1 = state.get('buttons_1', 0)
        hat = state.get('hat', -1)
        
        # Hat to D-Pad
        dpad_up = hat == 0 or hat == 1 or hat == 7
        dpad_right = hat == 1 or hat == 2 or hat == 3
        dpad_down = hat == 3 or hat == 4 or hat == 5
        dpad_left = hat == 5 or hat == 6 or hat == 7
        
        # Expanded Button Mapping
        # Xbox Controller: A, B, X, Y, LB, RB, LT, RT, Back, Start, L3, R3, D-Pad
        
        # Map Warthog Buttons (buttons_1 and buttons_2)
        # buttons_1: Trigger (1), Release (2), Pinky (4), Paddle (8), etc.
        # buttons_2: More buttons
        
        btn1 = state.get('buttons_1', 0)
        btn2 = state.get('buttons_2', 0)
        
        gamepad_data = {
            "axes": [
                state.get('joy_x', 0), # Left Stick X
                state.get('joy_y', 0), # Left Stick Y
                # Map Throttle to Right Stick Y for camera/other control if needed, or just keep 0
                0.0, # Right Stick X
                state.get('throttle_left', 0) * 2 - 1, # Right Stick Y (Mapped from Throttle L, -1 to 1)
            ],
            "buttons": [
                {"pressed": (btn1 & 0x01) > 0, "value": 1.0 if (btn1 & 0x01) else 0.0}, # A (Trigger)
                {"pressed": (btn1 & 0x02) > 0, "value": 1.0 if (btn1 & 0x02) else 0.0}, # B (Weapon Release)
                {"pressed": (btn1 & 0x04) > 0, "value": 1.0 if (btn1 & 0x04) else 0.0}, # X (Pinky)
                {"pressed": (btn1 & 0x08) > 0, "value": 1.0 if (btn1 & 0x08) else 0.0}, # Y (Paddle)
                {"pressed": (btn1 & 0x10) > 0, "value": 1.0 if (btn1 & 0x10) else 0.0}, # LB (Button 5)
                {"pressed": (btn1 & 0x20) > 0, "value": 1.0 if (btn1 & 0x20) else 0.0}, # RB (Button 6)
                {"pressed": state.get('throttle_left', 0) > 0.1, "value": state.get('throttle_left', 0)}, # LT (Throttle L)
                {"pressed": state.get('throttle_right', 0) > 0.1, "value": state.get('throttle_right', 0)}, # RT (Throttle R)
                {"pressed": (btn2 & 0x01) > 0, "value": 1.0 if (btn2 & 0x01) else 0.0}, # Back (Button 9)
                {"pressed": (btn2 & 0x02) > 0, "value": 1.0 if (btn2 & 0x02) else 0.0}, # Start (Button 10)
                {"pressed": (btn2 & 0x04) > 0, "value": 1.0 if (btn2 & 0x04) else 0.0}, # L3 (Button 11)
                {"pressed": (btn2 & 0x08) > 0, "value": 1.0 if (btn2 & 0x08) else 0.0}, # R3 (Button 12)
                {"pressed": dpad_up, "value": 1.0 if dpad_up else 0.0}, # Up
                {"pressed": dpad_down, "value": 1.0 if dpad_down else 0.0}, # Down
                {"pressed": dpad_left, "value": 1.0 if dpad_left else 0.0}, # Left
                {"pressed": dpad_right, "value": 1.0 if dpad_right else 0.0}, # Right
                {"pressed": False, "value": 0}, # Home
            ]
        }
        
        message = json.dumps(gamepad_data)
        if self.loop:
            # print(f"DEBUG: Broadcasting to {len(self.clients)} clients")
            future = asyncio.run_coroutine_threadsafe(self._broadcast_message(message), self.loop)
            # Optional: Check for immediate errors (though it's async)
            try:
                future.result(timeout=0.001)
            except asyncio.TimeoutError:
                pass # Expected, it takes time
            except Exception as e:
                print(f"DEBUG: Future error: {e}")
        else:
            print("DEBUG: No event loop!")

    async def _broadcast_message(self, message):
        # print(f"DEBUG: _broadcast_message running. Clients: {len(self.clients)}")
        if self.clients:
            # DEBUG: Inspect the first client to see what it is (one-time debug)
            # first_client = next(iter(self.clients))
            # print(f"DEBUG: Client attributes: {dir(first_client)}")

            # Safe filtering to avoid AttributeError
            active_clients = set()
            for c in self.clients:
                try:
                    # Check for 'open' or 'closed' attributes safely
                    if hasattr(c, 'open') and c.open:
                        active_clients.add(c)
                    elif hasattr(c, 'closed') and not c.closed:
                        active_clients.add(c)
                    elif hasattr(c, 'state'): # Check state if available
                        # 1 = OPEN
                        if c.state == 1: 
                            active_clients.add(c)
                    else:
                        # Fallback: assume open if we can't check, to avoid dropping valid connections
                        # print("DEBUG: Could not determine client state, assuming open")
                        active_clients.add(c)
                except Exception as e:
                    print(f"DEBUG: Error checking client state: {e}")
                    active_clients.add(c) # Keep on error to be safe

            self.clients = active_clients
            
            if self.clients:
                # print(f"DEBUG: Sending to {len(self.clients)} clients")
                try:
                    await asyncio.gather(*[client.send(message) for client in self.clients], return_exceptions=True)
                except Exception as e:
                    print(f"DEBUG: Send error: {e}")
                except Exception as e:
                    print(f"DEBUG: Send error: {e}")

    def _run_server(self):
        asyncio.run(self._async_server())

    async def _async_server(self):
        self.loop = asyncio.get_running_loop()
        print(f"Browser Bridge running on ws://127.0.0.1:{self.port}")
        async with websockets.serve(self._handler, "127.0.0.1", self.port):
            await asyncio.Future() # Run forever

    async def _handler(self, websocket):
        print("DEBUG: Client connected!")
        self.clients.add(websocket)
        try:
            await websocket.wait_closed()
        finally:
            print("DEBUG: Client disconnected!")
            self.clients.remove(websocket)
