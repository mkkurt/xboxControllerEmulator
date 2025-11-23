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
        self.server = None

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.loop and self.server:
            self.loop.call_soon_threadsafe(self.server.close)

    def broadcast(self, state):
        """
        Broadcast controller state to all connected browsers
        state format: {
            'uid_buttons': int,
            'uid_axis_0': float,
            'uid_hat': int,
            ...
        }
        """
        if not self.clients or not state:
            return
        
        # Convert universal state to Xbox gamepad format
        gamepad_data = self._convert_to_gamepad(state)
        message = json.dumps(gamepad_data)
        
        if self.loop:
            asyncio.run_coroutine_threadsafe(
                self._send_to_all(message), 
                self.loop
            )

    def _convert_to_gamepad(self, state):
        """
        Convert universal device state to standard Gamepad API format
        This is a smart converter that works with any configured device
        """
        # Initialize gamepad structure
        gamepad = {
            'axes': [0.0, 0.0, 0.0, 0.0],
            'buttons': [{'pressed': False, 'value': 0.0} for _ in range(17)]
        }

        # Map buttons from UniversalInputReader state
        # The state now contains keys like '{uid}_btn_A', '{uid}_btn_B', etc.

        button_map = {
            'A': 0, 'B': 1, 'X': 2, 'Y': 3,
            'LB': 4, 'RB': 5,
            'Back': 8, 'Start': 9,
            'L3': 10, 'R3': 11,
            'Guide': 16
        }

        # Iterate over all state keys to find button presses
        for key, value in state.items():
            if '_btn_' in key:
                # Extract button name (e.g., 'A' from '1234:5678_btn_A')
                btn_name = key.split('_btn_')[1]
                
                if btn_name in button_map:
                    idx = button_map[btn_name]
                    pressed = bool(value)
                    # OR with existing state to support multiple controllers mapping to same button
                    if pressed:
                        gamepad['buttons'][idx] = {'pressed': True, 'value': 1.0}
        
        # Map axes - Universal mapping based on calibrated axis names
        # Standard Xbox controller layout:
        # axes[0] = Left Stick X, axes[1] = Left Stick Y
        # axes[2] = Right Stick X, axes[3] = Right Stick Y
        # buttons[6] = Left Trigger (LT), buttons[7] = Right Trigger (RT)

        axis_map = {
            'LeftX': 0,
            'LeftY': 1,
            'RightX': 2,
            'RightY': 3,
            'LT': 6,  # Left Trigger as button
            'RT': 7   # Right Trigger as button
        }

        for key, value in state.items():
            # Check for calibrated axis names (format: uid_AxisName)
            for axis_name, gamepad_index in axis_map.items():
                if f'_{axis_name}' in key:
                    if axis_name in ['LT', 'RT']:
                        # Triggers are buttons with analog values (0.0 to 1.0)
                        val = max(0.0, min(1.0, value))
                        gamepad['buttons'][gamepad_index] = {'pressed': val > 0.1, 'value': val}
                    else:
                        # Stick axes
                        gamepad['axes'][gamepad_index] = float(value)
        
        # Map D-Pad from hat
        for key, value in state.items():
            if '_hat' in key and isinstance(value, int):
                hat = value
                gamepad['buttons'][12] = {'pressed': hat in [0, 1, 7], 'value': 1.0 if hat in [0, 1, 7] else 0.0}  # Up
                gamepad['buttons'][13] = {'pressed': hat in [3, 4, 5], 'value': 1.0 if hat in [3, 4, 5] else 0.0}  # Down
                gamepad['buttons'][14] = {'pressed': hat in [5, 6, 7], 'value': 1.0 if hat in [5, 6, 7] else 0.0}  # Left
                gamepad['buttons'][15] = {'pressed': hat in [1, 2, 3], 'value': 1.0 if hat in [1, 2, 3] else 0.0}  # Right
        
        return gamepad

    async def _send_to_all(self, message):
        if self.clients:
            await asyncio.gather(
                *[client.send(message) for client in self.clients],
                return_exceptions=True
            )

    def _run_server(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        async def handler(websocket):
            self.clients.add(websocket)
            print("DEBUG: Client connected!")
            try:
                await websocket.wait_closed()
            finally:
                self.clients.remove(websocket)
                print("DEBUG: Client disconnected!")
        
        async def serve():
            self.server = await websockets.serve(handler, "127.0.0.1", self.port)
            print(f"Browser Bridge running on ws://127.0.0.1:{self.port}")
            await asyncio.Future()  # run forever
        
        self.loop.run_until_complete(serve())
