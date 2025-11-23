from PyQt6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox
from ui.curve_editor import CurveEditor

class InputConfigDialog(QDialog):
    """Dialog for advanced input configuration"""
    def __init__(self, device_manager, device, parent=None):
        super().__init__(parent)
        self.device_manager = device_manager
        self.device = device
        self.setWindowTitle(f"Configure {device.product}")
        self.setMinimumSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # Curve Editor
        self.editor = CurveEditor()
        
        # Load existing config
        config = self.device_manager.get_device_config(device) or {}
        if 'processing' in config:
            self.editor.set_config(config['processing'])
            
        self.editor.config_changed.connect(self.save_config)
        layout.addWidget(self.editor)
        
        # Close button
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.accept)
        layout.addWidget(buttons)
        
    def save_config(self, processing_config):
        # Get full config
        config = self.device_manager.get_device_config(self.device) or {}
        config['processing'] = processing_config
        
        # Save
        self.device_manager.save_device_config(self.device, config)
        
        # Update active processor if running
        if self.parent() and hasattr(self.parent(), 'reader'):
            if self.device.uid in self.parent().reader.processors:
                self.parent().reader.processors[self.device.uid].update_config(processing_config)
