"""
Curve Editor Widget
Visualizes and edits input response curves.
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QSlider, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal, QPointF
from PyQt6.QtGui import QPainter, QPen, QColor, QPainterPath, QBrush
from ui.theme import Theme
import math

class CurveGraph(QWidget):
    """Visualizes the response curve"""
    def __init__(self):
        super().__init__()
        self.setMinimumSize(200, 200)
        self.config = {'deadzone': 0.05, 'curve': 1.0, 'smoothing': 0.0}
        self.setStyleSheet(f"background-color: {Theme.MANTLE}; border-radius: 6px;")

    def update_config(self, config):
        self.config = config
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w = self.width()
        h = self.height()
        
        # Draw Grid
        painter.setPen(QPen(QColor(Theme.SURFACE0), 1))
        # Center lines
        painter.drawLine(w//2, 0, w//2, h)
        painter.drawLine(0, h//2, w, h//2)
        
        # Draw Deadzone Area
        dz = self.config['deadzone']
        if dz > 0:
            dz_w = w * dz / 2  # Half width because graph is -1 to 1
            painter.fillRect(int(w/2 - dz_w), 0, int(dz_w * 2), h, QColor(Theme.SURFACE0))
        
        # Draw Curve
        path = QPainterPath()
        
        # Generate points
        steps = 100
        for i in range(steps + 1):
            # Input -1.0 to 1.0
            x_norm = (i / steps) * 2.0 - 1.0
            
            # Calculate output using same logic as InputProcessor
            y_norm = self._calculate_output(x_norm)
            
            # Map to screen coordinates
            # X: -1..1 -> 0..w
            # Y: -1..1 -> h..0 (inverted Y)
            px = (x_norm + 1) / 2 * w
            py = h - ((y_norm + 1) / 2 * h)
            
            if i == 0:
                path.moveTo(px, py)
            else:
                path.lineTo(px, py)
        
        painter.setPen(QPen(QColor(Theme.BLUE), 2))
        painter.drawPath(path)
        
    def _calculate_output(self, value):
        # Deadzone
        dz = self.config['deadzone']
        if abs(value) < dz:
            return 0.0
        
        sign = 1.0 if value > 0 else -1.0
        normalized = (abs(value) - dz) / (1.0 - dz)
        value = sign * normalized
        
        # Curve
        curve = self.config['curve']
        if curve != 1.0:
            value = sign * (abs(value) ** curve)
            
        return value

class CurveEditor(QWidget):
    """Editor with sliders and graph"""
    config_changed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.config = {'deadzone': 0.05, 'curve': 1.0, 'smoothing': 0.0}
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Left: Graph
        self.graph = CurveGraph()
        layout.addWidget(self.graph, 1)
        
        # Right: Controls
        controls = QWidget()
        controls.setFixedWidth(200)
        c_layout = QVBoxLayout(controls)
        
        # Deadzone Slider
        c_layout.addWidget(QLabel("Deadzone"))
        self.dz_slider = self._create_slider(0, 50, int(self.config['deadzone']*100))
        self.dz_label = QLabel(f"{self.config['deadzone']:.2f}")
        c_layout.addWidget(self.dz_slider)
        c_layout.addWidget(self.dz_label)
        
        # Curve Slider
        c_layout.addWidget(QLabel("Response Curve"))
        # Map 1.0-3.0 to 0-200
        self.curve_slider = self._create_slider(0, 200, int((self.config['curve']-1)*100))
        self.curve_label = QLabel(f"{self.config['curve']:.2f}")
        c_layout.addWidget(self.curve_slider)
        c_layout.addWidget(self.curve_label)
        
        # Smoothing Slider
        c_layout.addWidget(QLabel("Smoothing"))
        self.smooth_slider = self._create_slider(0, 90, int(self.config['smoothing']*100))
        self.smooth_label = QLabel(f"{self.config['smoothing']:.2f}")
        c_layout.addWidget(self.smooth_slider)
        c_layout.addWidget(self.smooth_label)
        
        c_layout.addStretch()
        layout.addWidget(controls)
        
        # Connect signals
        self.dz_slider.valueChanged.connect(self._on_change)
        self.curve_slider.valueChanged.connect(self._on_change)
        self.smooth_slider.valueChanged.connect(self._on_change)
        
    def _create_slider(self, min_val, max_val, current):
        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(min_val, max_val)
        slider.setValue(current)
        return slider
        
    def _on_change(self):
        self.config['deadzone'] = self.dz_slider.value() / 100.0
        self.config['curve'] = 1.0 + (self.curve_slider.value() / 100.0)
        self.config['smoothing'] = self.smooth_slider.value() / 100.0
        
        # Update labels
        self.dz_label.setText(f"{self.config['deadzone']:.2f}")
        self.curve_label.setText(f"{self.config['curve']:.2f}")
        self.smooth_label.setText(f"{self.config['smoothing']:.2f}")
        
        # Update graph
        self.graph.update_config(self.config)
        
        # Emit signal
        self.config_changed.emit(self.config)

    def set_config(self, config):
        """Load config into UI"""
        self.config = config.copy()
        self.dz_slider.setValue(int(self.config.get('deadzone', 0.05) * 100))
        self.curve_slider.setValue(int((self.config.get('curve', 1.0) - 1.0) * 100))
        self.smooth_slider.setValue(int(self.config.get('smoothing', 0.0) * 100))
        self.graph.update_config(self.config)
