from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QProgressBar,
    QHBoxLayout, QFrame
)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
import hid
from ui.calibration_logic import CalibrationLogic

class CalibrationDialog(QDialog):
    """
    Improved calibration wizard with 2-stage process:
    1. Axis Calibration (Sticks & Triggers)
    2. Button Mapping
    """
    def __init__(self, device_manager, parent=None):
        super().__init__(parent)
        self.device_manager = device_manager
        self.logic = CalibrationLogic()

        self.devices = []
        self.current_device = None
        self.hid_device = None

        # State tracking
        self.stage = "INIT" # INIT, AXIS, AXIS_MAPPING, BUTTONS, FINISHED
        self.xbox_buttons = ['A', 'B', 'X', 'Y', 'LB', 'RB', 'Back', 'Start', 'Guide', 'L3', 'R3']
        self.xbox_axes = [
            ('Left Stick X', 'LeftX'),
            ('Left Stick Y', 'LeftY'),
            ('Right Stick X', 'RightX'),
            ('Right Stick Y', 'RightY'),
            ('Left Trigger', 'LT'),
            ('Right Trigger', 'RT')
        ]
        self.current_button_index = 0
        self.current_axis_index = 0
        self.mapped_axes = {} # name -> {offset, min, max, center}

        # Anti-skip protection
        self.detection_enabled = False  # Only detect when ready
        self.last_detection_time = 0   # For cooldown
        self.detection_cooldown = 0.5   # Minimum 500ms between detections
        
        self.setup_ui()
        self.start_wizard()
    
    def setup_ui(self):
        self.setWindowTitle("Controller Calibration Wizard")
        self.setMinimumSize(700, 600)
        self.setStyleSheet("""
            QDialog { background-color: #1e1e2e; }
            QLabel { color: #cdd6f4; }
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: 600;
                font-size: 14px;
                min-height: 40px;
            }
            QPushButton:hover { background-color: #b4befe; }
            QPushButton:disabled { background-color: #45475a; color: #6c7086; }
            QTextEdit {
                background-color: #181825;
                border: 1px solid #313244;
                border-radius: 6px;
                padding: 12px;
                color: #a6e3a1;
                font-family: monospace;
            }
            QProgressBar {
                border: 2px solid #313244;
                border-radius: 5px;
                text-align: center;
                background-color: #181825;
            }
            QProgressBar::chunk { background-color: #a6e3a1; }
            QFrame#StepFrame {
                background-color: #181825;
                border: 1px solid #313244;
                border-radius: 8px;
                padding: 16px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        self.title_label = QLabel("🎮 Calibration Wizard")
        self.title_label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title_label.setStyleSheet("color: #89b4fa;")
        layout.addWidget(self.title_label)
        
        # Step Indicator
        self.step_label = QLabel("Step 1 of 3: Axis Calibration")
        self.step_label.setFont(QFont("Arial", 12))
        self.step_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.step_label.setStyleSheet("color: #a6adc8;")
        layout.addWidget(self.step_label)
        
        # Main Content Area
        self.content_frame = QFrame()
        self.content_frame.setObjectName("StepFrame")
        content_layout = QVBoxLayout(self.content_frame)
        
        self.instruction_label = QLabel("Initializing...")
        self.instruction_label.setFont(QFont("Arial", 16))
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instruction_label.setWordWrap(True)
        self.instruction_label.setStyleSheet("margin: 20px 0;")
        content_layout.addWidget(self.instruction_label)
        
        # Visualization / Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(10)
        content_layout.addWidget(self.progress_bar)
        
        layout.addWidget(self.content_frame)
        
        # Log
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(self.log_text)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet("background-color: #f38ba8;")
        self.cancel_btn.clicked.connect(self.reject)
        controls_layout.addWidget(self.cancel_btn)
        
        controls_layout.addStretch()
        
        self.action_btn = QPushButton("Start")
        self.action_btn.clicked.connect(self.on_action_clicked)
        controls_layout.addWidget(self.action_btn)
        
        layout.addLayout(controls_layout)
        self.setLayout(layout)
        
        # Timer for reading input
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_input)

    def start_wizard(self):
        self.devices = self.device_manager.scan_devices()
        if not self.devices:
            self.instruction_label.setText("No controller detected!\nPlease connect a device.")
            self.action_btn.setEnabled(False)
            return
            
        self.current_device = self.devices[0]
        self.log(f"Detected: {self.current_device}")
        
        try:
            # Open device
            vid_pid = self.current_device.uid
            vid, pid = [int(x, 16) for x in vid_pid.split(':')]
            
            self.hid_device = hid.device()
            self.hid_device.open(vid, pid)
            self.hid_device.set_nonblocking(1)
            self.log(f"Connected to device {vid_pid}")
            
            self.start_axis_stage()
            
        except Exception as e:
            self.log(f"Error opening device: {e}")
            self.instruction_label.setText("Failed to open device.")
            self.action_btn.setEnabled(False)

    def start_axis_stage(self):
        self.stage = "AXIS"
        self.step_label.setText("Step 1 of 3: Axis Range Calibration")
        self.instruction_label.setText(
            "Move all sticks in full circles.\n"
            "Press all triggers fully.\n\n"
            "Click 'Next' when done."
        )
        self.action_btn.setText("Next")
        self.progress_bar.setValue(0)
        self.logic.reset()
        self.timer.start(16) # ~60Hz

    def start_axis_mapping_stage(self):
        self.stage = "AXIS_MAPPING"
        self.step_label.setText("Step 2 of 3: Axis Mapping")

        # Finalize axes first
        self.axes_config = self.logic.finalize_axes()
        self.log(f"Detected {len(self.axes_config)} potential axes")

        if not self.axes_config:
            self.log("No axes detected! Please try again.")
            self.start_axis_stage()
            return

        # Reset detection state for axis mapping
        self.detection_enabled = False
        self.last_detection_time = 0
        self.logic.baseline_data = None

        self.current_axis_index = 0
        self.update_axis_instruction()
        self.action_btn.setText("Skip")

    def update_axis_instruction(self):
        if self.current_axis_index >= len(self.xbox_axes):
            self.start_button_stage()
            return

        # DISABLE detection while showing instruction
        self.detection_enabled = False

        pretty_name, _ = self.xbox_axes[self.current_axis_index]
        self.instruction_label.setText(f"Move/Press: {pretty_name}\n\n(Ready in 1 second...)")

        progress = (self.current_axis_index / len(self.xbox_axes)) * 100
        self.progress_bar.setValue(int(progress))

        # Reset baseline for new axis detection
        self.logic.baseline_data = None

        # Enable detection after 1 second delay
        QTimer.singleShot(1000, self._enable_axis_detection)

    def start_button_stage(self):
        self.stage = "BUTTONS"
        self.step_label.setText("Step 3 of 3: Button Mapping")

        # Reset detection state for button mapping
        self.detection_enabled = False
        self.last_detection_time = 0
        self.logic.baseline_data = None

        self.current_button_index = 0
        self.update_button_instruction()
        self.action_btn.setText("Skip")

    def update_button_instruction(self):
        if self.current_button_index >= len(self.xbox_buttons):
            self.finish_calibration()
            return

        # DISABLE detection while showing instruction
        self.detection_enabled = False

        btn_name = self.xbox_buttons[self.current_button_index]
        self.instruction_label.setText(f"Press button: {btn_name}\n\n(Ready in 1 second...)\nRelease all buttons!")

        progress = (self.current_button_index / len(self.xbox_buttons)) * 100
        self.progress_bar.setValue(int(progress))

        # Baseline will be captured in _enable_button_detection after 1 second
        # This gives user time to release any pressed buttons

        # Enable detection after 1 second delay
        QTimer.singleShot(1000, self._enable_button_detection)

    def _enable_axis_detection(self):
        """Enable axis detection after delay"""
        self.detection_enabled = True
        pretty_name, _ = self.xbox_axes[self.current_axis_index]
        self.instruction_label.setText(f"Move/Press: {pretty_name}\n\n✓ Ready! Move the axis now.")

    def _enable_button_detection(self):
        """Enable button detection after delay"""
        # Capture baseline NOW (when user is NOT pressing anything)
        try:
            data = self.hid_device.read(64)
            if data:
                self.logic.baseline_data = bytes(data)
                # Debug: show baseline
                hex_str = ' '.join(f'{b:02x}' for b in data[:16])
                self.log(f"Baseline captured: [{hex_str}...]")
        except Exception as e:
            self.log(f"Failed to capture baseline: {e}")

        self.detection_enabled = True
        btn_name = self.xbox_buttons[self.current_button_index]
        self.instruction_label.setText(f"Press button: {btn_name}\n\n✓ Ready! Press the button now.")

    def process_input(self):
        if not self.hid_device:
            return

        try:
            data = self.hid_device.read(64)
            if not data:
                return

            if self.stage == "AXIS":
                self.logic.process_axis_calibration(data)

            elif self.stage == "AXIS_MAPPING":
                # Only detect if enabled and cooldown passed
                if not self.detection_enabled:
                    return

                import time
                current_time = time.time()
                if current_time - self.last_detection_time < self.detection_cooldown:
                    return

                result = self.logic.detect_axis_movement(data, self.axes_config)
                if result:
                    byte_index, value = result
                    self.last_detection_time = current_time
                    self.on_axis_detected(byte_index, value)

            elif self.stage == "BUTTONS":
                # Only detect if enabled and cooldown passed
                if not self.detection_enabled:
                    return

                import time
                current_time = time.time()
                if current_time - self.last_detection_time < self.detection_cooldown:
                    return

                # Pass mapped axes to exclude them from button detection
                mapped_byte_indices = {cfg['offset'] for cfg in self.mapped_axes.values()}
                result = self.logic.detect_button(data, self.axes_config, mapped_byte_indices)
                if result:
                    byte_index, value = result
                    self.last_detection_time = current_time
                    # Show filter reason if available
                    if hasattr(self.logic, 'last_filter_reason'):
                        self.log(f"Detection: {self.logic.last_filter_reason}")
                    self.on_button_detected(byte_index, value)
                # Debug: show detection info periodically
                elif hasattr(self.logic, 'last_candidates_count'):
                    count = self.logic.last_candidates_count
                    if count > 1:
                        # Show which bytes changed
                        if hasattr(self.logic, 'last_candidates'):
                            changes = ', '.join(f"byte {i}={v:02x}" for i, v in self.logic.last_candidates[:5])
                            self.log(f"Multiple changes ({count}): {changes}")

        except Exception as e:
            self.log(f"Read error: {e}")

    def on_axis_detected(self, byte_index, value):
        pretty_name, internal_name = self.xbox_axes[self.current_axis_index]

        # Check if already mapped
        for mapped in self.mapped_axes.values():
            if mapped['offset'] == byte_index:
                return # Already mapped to something else

        # Get stats from config
        stats = self.axes_config[byte_index]

        self.mapped_axes[internal_name] = {
            'offset': byte_index,
            'min': stats['min'],
            'max': stats['max'],
            'center': stats['center'],
            'deadzone': stats['deadzone']
        }

        self.log(f"✓ Mapped {pretty_name} -> Byte {byte_index}")

        # DISABLE detection before advancing
        self.detection_enabled = False

        self.current_axis_index += 1
        self.update_axis_instruction()

    def on_button_detected(self, byte_index, value):
        btn_name = self.xbox_buttons[self.current_button_index]
        self.logic.button_mappings[btn_name] = [byte_index, value]
        self.log(f"✓ Mapped {btn_name} -> Byte {byte_index} = {value}")

        # DISABLE detection before advancing
        self.detection_enabled = False

        self.current_button_index += 1
        self.update_button_instruction()

    def on_action_clicked(self):
        if self.stage == "AXIS":
            self.start_axis_mapping_stage()
        elif self.stage == "AXIS_MAPPING":
            # Skip current axis
            pretty_name, _ = self.xbox_axes[self.current_axis_index]
            self.log(f"Skipped {pretty_name}")
            self.current_axis_index += 1
            self.update_axis_instruction()
        elif self.stage == "BUTTONS":
            # Skip current button
            btn_name = self.xbox_buttons[self.current_button_index]
            self.log(f"Skipped {btn_name}")
            self.current_button_index += 1
            self.update_button_instruction()
        elif self.stage == "FINISHED":
            self.accept()

    def finish_calibration(self):
        self.stage = "FINISHED"
        self.timer.stop()
        if self.hid_device:
            self.hid_device.close()
            
        self.instruction_label.setText("Calibration Complete!")
        self.action_btn.setText("Finish")
        self.cancel_btn.hide()
        self.progress_bar.setValue(100)
        
        # Save config
        config = {
            'device_id': str(self.current_device),
            'mappings': {
                'axes': self.mapped_axes,
                'buttons': {} # Legacy format requires this? No, universal_reader checks 'button_map' too
            },
            'button_map': self.logic.button_mappings
        }
        
        # Also save legacy mappings for compatibility if needed
        # But universal_reader.py was updated to check 'button_map'
        # Wait, I need to check universal_reader.py again.
        # It checks: if 'button_map' in config: ...
        # And: if 'axes' in mappings: ...
        
        self.device_manager.save_device_config(self.current_device, config)
        self.log("Configuration saved.")

    def log(self, msg):
        self.log_text.append(f"• {msg}")
