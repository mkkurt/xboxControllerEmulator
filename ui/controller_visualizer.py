"""
Controller Visualizer Widget
Renders a real-time view of the virtual Xbox controller.
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPointF, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QBrush, QPainterPath
from ui.theme import Theme

class ControllerVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(300, 200)
        self.state = {}  # Current input state
        
    def update_state(self, state):
        """Update visualizer with new input state"""
        self.state = state
        self.update()
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        scale = min(w/300, h/200)
        
        painter.translate(w/2, h/2)
        painter.scale(scale, scale)
        
        # Draw Body
        self._draw_body(painter)
        
        # Draw Triggers/Bumpers
        self._draw_triggers(painter)
        
        # Draw Sticks
        self._draw_sticks(painter)
        
        # Draw Buttons
        self._draw_buttons(painter)
        
        # Draw D-Pad
        self._draw_dpad(painter)

    def _draw_body(self, painter):
        path = QPainterPath()
        path.addRoundedRect(-140, -90, 280, 180, 40, 40)
        
        painter.setPen(QPen(QColor(Theme.SURFACE0), 2))
        painter.setBrush(QBrush(QColor(Theme.MANTLE)))
        painter.drawPath(path)

    def _draw_buttons(self, painter):
        # ABXY Cluster
        buttons = {
            'A': (80, 40, Theme.GREEN),
            'B': (110, 10, Theme.RED),
            'X': (50, 10, Theme.BLUE),
            'Y': (80, -20, Theme.YELLOW)
        }
        
        for name, (x, y, color) in buttons.items():
            pressed = self._is_pressed(name)
            
            painter.setPen(Qt.PenStyle.NoPen)
            if pressed:
                painter.setBrush(QColor(color))
            else:
                painter.setBrush(QColor(Theme.SURFACE1))
                
            painter.drawEllipse(QPointF(x, y), 12, 12)
            
            # Label
            painter.setPen(QColor(Theme.BASE if pressed else Theme.TEXT))
            painter.drawText(QRectF(x-12, y-12, 24, 24), Qt.AlignmentFlag.AlignCenter, name)

    def _draw_sticks(self, painter):
        # Left Stick (Top Left)
        lx = self._get_axis('LX') * 20
        ly = -self._get_axis('LY') * 20  # Invert Y for screen coords
        
        painter.setPen(QPen(QColor(Theme.SURFACE0), 2))
        painter.setBrush(QColor(Theme.SURFACE1))
        painter.drawEllipse(QPointF(-80, -20), 25, 25)  # Base
        
        painter.setBrush(QColor(Theme.BLUE))
        painter.drawEllipse(QPointF(-80 + lx, -20 + ly), 15, 15)  # Stick
        
        # Right Stick (Bottom Right)
        rx = self._get_axis('RX') * 20
        ry = -self._get_axis('RY') * 20
        
        painter.setBrush(QColor(Theme.SURFACE1))
        painter.drawEllipse(QPointF(40, 40), 25, 25)  # Base
        
        painter.setBrush(QColor(Theme.BLUE))
        painter.drawEllipse(QPointF(40 + rx, 40 + ry), 15, 15)  # Stick

    def _draw_dpad(self, painter):
        x, y = -50, 40
        size = 15
        
        # Cross shape
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(Theme.SURFACE1))
        painter.drawRect(int(x-size/2), int(y-size*1.5), size, size*3)
        painter.drawRect(int(x-size*1.5), int(y-size/2), size*3, size)
        
        # Highlight pressed direction
        hat = self.state.get('hat', -1)
        # TODO: Map hat directions to visual highlights

    def _draw_triggers(self, painter):
        # LT
        lt = self._get_axis('LT') # 0 to 1
        painter.setBrush(QColor(Theme.SURFACE1))
        painter.drawRect(-120, -110, 40, 15)
        if lt > 0.1:
            painter.setBrush(QColor(Theme.BLUE))
            painter.drawRect(-120, -110, int(40 * lt), 15)
            
        # RT
        rt = self._get_axis('RT')
        painter.setBrush(QColor(Theme.SURFACE1))
        painter.drawRect(80, -110, 40, 15)
        if rt > 0.1:
            painter.setBrush(QColor(Theme.BLUE))
            painter.drawRect(80, -110, int(40 * rt), 15)

    def _is_pressed(self, btn_name):
        # Check state for button press
        # State keys are like 'UID_btn_A'
        for key, val in self.state.items():
            if key.endswith(f"_btn_{btn_name}") and val:
                return True
        return False

    def _get_axis(self, axis_name):
        # Check state for axis value
        for key, val in self.state.items():
            if key.endswith(f"_{axis_name}"):
                return val
        return 0.0
