from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QDialogButtonBox
from ui.controller_visualizer import ControllerVisualizer

class TestDialog(QDialog):
    """Dialog for testing controller input"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Test Controller")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        self.visualizer = ControllerVisualizer()
        layout.addWidget(self.visualizer)
        
        layout.addWidget(QLabel("Press buttons and move sticks to test."))
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.accept)
        layout.addWidget(buttons)
        
    def update_state(self, state):
        self.visualizer.update_state(state)
