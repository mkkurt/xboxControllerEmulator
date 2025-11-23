import Quartz
import time

class OutputEmulator:
    # Virtual Key Codes for macOS
    VK_A = 0x00
    VK_S = 0x01
    VK_D = 0x02
    VK_W = 0x0D
    VK_SPACE = 0x31
    
    def __init__(self):
        self.pressed_keys = set()
        self.mouse_x = 0
        self.mouse_y = 0

    def update(self, state):
        """
        Updates the output based on the input state.
        state: dict with 'joy_x', 'joy_y', 'throttle_left', 'throttle_right', 'buttons'
        """
        # Joystick X -> A/D
        if state['joy_x'] < -0.5:
            self._press_key(self.VK_A)
            self._release_key(self.VK_D)
        elif state['joy_x'] > 0.5:
            self._press_key(self.VK_D)
            self._release_key(self.VK_A)
        else:
            self._release_key(self.VK_A)
            self._release_key(self.VK_D)

        # Joystick Y -> W/S
        if state['joy_y'] < -0.5: # Forward (negative Y usually)
            self._press_key(self.VK_W)
            self._release_key(self.VK_S)
        elif state['joy_y'] > 0.5: # Backward
            self._press_key(self.VK_S)
            self._release_key(self.VK_W)
        else:
            self._release_key(self.VK_W)
            self._release_key(self.VK_S)

        # TODO: Map buttons

    def _press_key(self, key_code):
        if key_code not in self.pressed_keys:
            self._post_key_event(key_code, True)
            self.pressed_keys.add(key_code)

    def _release_key(self, key_code):
        if key_code in self.pressed_keys:
            self._post_key_event(key_code, False)
            self.pressed_keys.remove(key_code)

    def _post_key_event(self, key_code, down):
        event = Quartz.CGEventCreateKeyboardEvent(None, key_code, down)
        Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)

    def move_mouse(self, dx, dy):
        # Implementation for mouse movement if needed
        pass
