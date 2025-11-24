from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit, QProgressBar,
    QHBoxLayout, QFrame, QWidget
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
import hid
import time
from ui.calibration_logic import CalibrationLogic

class SimpleCalibrationDialog(QDialog):
    """
    Simple, robust calibration wizard
    - Clear instructions
    - Manual progression (no auto-advance)
    - Real-time feedback
    - Retry capability
    """
    def __init__(self, device_manager, parent=None):
        super().__init__(parent)
        self.device_manager = device_manager
        self.logic = CalibrationLogic()

        # Device
        self.devices = []
        self.current_device = None
        self.hid_device = None

        # Calibration state
        self.step = 0  # Current step number
        self.max_steps = 3  # Total steps
        self.mapped_axes = {}
        self.button_mappings = {}

        # Detection state
        self.waiting_for_input = False
        self.detection_enabled = False  # Gatekeeper for input processing
        self.current_target = None  # What we're currently trying to detect
        self.last_detection_time = 0

        # Timers
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_input)

        self.ready_timer = QTimer()
        self.ready_timer.setSingleShot(True)

        # Step definitions
        self.steps = [
            {
                'title': 'Step 1: Axis Range Calibration',
                'instruction': 'Move all sticks in FULL circles.\nPress all triggers FULLY.\n\nThen click NEXT.',
                'action': 'calibrate_axes',
                'button': 'Next →'
            },
            {
                'title': 'Step 2: Map Your Axes',
                'instruction': 'Click "Start" then move each axis when asked.',
                'action': 'map_axes',
                'button': 'Start'
            },
            {
                'title': 'Step 3: Map Your Buttons',
                'instruction': 'Click "Start" then press each button when asked.',
                'action': 'map_buttons',
                'button': 'Start'
            }
        ]

        # Axis and button lists
        self.xbox_axes = [
            ('Left Stick X', 'LeftX'),
            ('Left Stick Y', 'LeftY'),
            ('Right Stick X', 'RightX'),
            ('Right Stick Y', 'RightY'),
            ('Left Trigger', 'LT'),
            ('Right Trigger', 'RT')
        ]
        self.xbox_buttons = ['A', 'B', 'X', 'Y', 'LB', 'RB', 'Back', 'Start', 'Guide', 'L3', 'R3']

        self.setup_ui()
        self.init_device()
        self.show_current_step()

    def setup_ui(self):
        self.setWindowTitle("Controller Calibration")
        self.setMinimumSize(800, 650)
        self.setStyleSheet("""
            QDialog { background-color: #1e1e2e; }
            QLabel { color: #cdd6f4; }
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                border-radius: 8px;
                padding: 15px 30px;
                font-weight: 600;
                font-size: 15px;
                min-height: 50px;
            }
            QPushButton:hover { background-color: #b4befe; }
            QPushButton:disabled { background-color: #45475a; color: #6c7086; }
            QPushButton#SkipButton {
                background-color: #f9e2af;
                color: #1e1e2e;
            }
            QPushButton#SkipButton:hover { background-color: #f5e0d0; }
            QTextEdit {
                background-color: #181825;
                border: 1px solid #313244;
                border-radius: 6px;
                padding: 12px;
                color: #a6e3a1;
                font-family: 'Monaco', 'Courier New', monospace;
                font-size: 12px;
            }
            QProgressBar {
                border: 2px solid #313244;
                border-radius: 5px;
                text-align: center;
                background-color: #181825;
                color: #cdd6f4;
                font-weight: bold;
            }
            QProgressBar::chunk { background-color: #a6e3a1; }
            QFrame#ContentFrame {
                background-color: #181825;
                border: 2px solid #313244;
                border-radius: 12px;
                padding: 30px;
            }
        """)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("🎮 Controller Calibration")
        title.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #89b4fa; margin-bottom: 10px;")
        main_layout.addWidget(title)

        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setFixedHeight(15)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(self.max_steps)
        self.progress_bar.setValue(self.step)
        self.progress_bar.setFormat("Step %v of %m")
        main_layout.addWidget(self.progress_bar)

        # Content frame
        self.content_frame = QFrame()
        self.content_frame.setObjectName("ContentFrame")
        content_layout = QVBoxLayout(self.content_frame)
        content_layout.setSpacing(20)

        # Step title
        self.step_title = QLabel("Step 1: Axis Calibration")
        self.step_title.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.step_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.step_title.setStyleSheet("color: #f9e2af;")
        content_layout.addWidget(self.step_title)

        # Instruction
        self.instruction_label = QLabel("Initializing...")
        self.instruction_label.setFont(QFont("Arial", 14))
        self.instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.instruction_label.setWordWrap(True)
        self.instruction_label.setMinimumHeight(120)
        self.instruction_label.setStyleSheet("color: #cdd6f4; line-height: 1.6;")
        content_layout.addWidget(self.instruction_label)

        # Status/Feedback
        self.status_label = QLabel("")
        self.status_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setMinimumHeight(60)
        self.status_label.setWordWrap(True)
        content_layout.addWidget(self.status_label)

        main_layout.addWidget(self.content_frame)

        # Activity log
        log_label = QLabel("Activity Log:")
        log_label.setStyleSheet("color: #a6adc8; font-size: 12px;")
        main_layout.addWidget(log_label)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(120)
        main_layout.addWidget(self.log_text)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)

        self.cancel_btn = QPushButton("✕ Cancel")
        self.cancel_btn.setStyleSheet("background-color: #f38ba8;")
        self.cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_btn)

        button_layout.addStretch()

        self.skip_btn = QPushButton("Skip")
        self.skip_btn.setObjectName("SkipButton")
        self.skip_btn.clicked.connect(self.on_skip_clicked)
        self.skip_btn.hide()
        button_layout.addWidget(self.skip_btn)

        self.action_btn = QPushButton("Next →")
        self.action_btn.clicked.connect(self.on_action_clicked)
        button_layout.addWidget(self.action_btn)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

    def init_device(self):
        """Initialize and open the device"""
        self.devices = self.device_manager.scan_devices()
        if not self.devices:
            self.log("✗ No controller detected!")
            self.instruction_label.setText("No controller found.\nPlease connect a controller and restart.")
            self.action_btn.setEnabled(False)
            return False

        self.current_device = self.devices[0]
        self.log(f"✓ Found: {self.current_device}")

        try:
            vid_pid = self.current_device.uid
            vid, pid = [int(x, 16) for x in vid_pid.split(':')]

            self.hid_device = hid.device()
            self.hid_device.open(vid, pid)
            self.hid_device.set_nonblocking(1)
            self.log(f"✓ Connected to {vid_pid}")
            return True

        except Exception as e:
            self.log(f"✗ Failed to open device: {e}")
            self.instruction_label.setText("Failed to open controller.\nPlease check permissions and restart.")
            self.action_btn.setEnabled(False)
            return False

    def show_current_step(self):
        """Display the current calibration step"""
        if self.step >= self.max_steps:
            self.finish_calibration()
            return

        step_info = self.steps[self.step]

        # Update UI
        self.progress_bar.setValue(self.step + 1)
        self.step_title.setText(step_info['title'])
        self.instruction_label.setText(step_info['instruction'])
        self.action_btn.setText(step_info['button'])
        self.status_label.setText("")

        # Reset state
        self.waiting_for_input = False
        self.detection_enabled = False
        self.skip_btn.hide()

        # Start timer for step 1 (axis calibration)
        if self.step == 0:
            self.logic.reset()
            self.timer.start(16)  # ~60 Hz

    def on_action_clicked(self):
        """Handle main action button click"""
        if self.step == 0:
            # Axis calibration - advance to axis mapping
            self.timer.stop()
            self.axes_config = self.logic.finalize_axes()
            self.log(f"✓ Detected {len(self.axes_config)} axes with movement")

            if len(self.axes_config) < 2:
                self.status_label.setText("⚠ Not enough movement detected!\nPlease try again.")
                self.status_label.setStyleSheet("color: #f38ba8;")
                self.logic.reset()
                self.timer.start(16)
                return

            self.step += 1
            self.show_current_step()

        elif self.step == 1:
            # Start axis mapping
            if not self.waiting_for_input:
                self.start_axis_mapping()

        elif self.step == 2:
            # Start button mapping
            if not self.waiting_for_input:
                self.start_button_mapping()

    def on_skip_clicked(self):
        """Skip current axis/button"""
        # Cancel any pending ready timer
        self.ready_timer.stop()

        if self.step == 1:
            # Skip axis
            self.axis_map_index += 1
            self.next_axis_mapping()
        elif self.step == 2:
            # Skip button
            self.button_map_index += 1
            self.next_button_mapping()

    def start_axis_mapping(self):
        """Begin the axis mapping process"""
        self.waiting_for_input = True
        self.axis_map_index = 0
        self.skip_btn.show()
        self.action_btn.hide()
        self.timer.start(16)
        self.next_axis_mapping()

    def next_axis_mapping(self):
        """Show next axis to map"""
        # Stop any pending timer
        self.ready_timer.stop()

        if self.axis_map_index >= len(self.xbox_axes):
            # Done with axes
            self.timer.stop()
            self.skip_btn.hide()
            self.action_btn.show()
            self.status_label.setText("✓ Axis mapping complete!")
            self.status_label.setStyleSheet("color: #a6e3a1;")
            self.log(f"✓ Mapped {len(self.mapped_axes)} axes")

            # Advance to next step
            self.step += 1
            QTimer.singleShot(1500, self.show_current_step)
            return

        pretty_name, internal_name = self.xbox_axes[self.axis_map_index]
        self.current_target = internal_name

        self.instruction_label.setText(f"Move or press:\n{pretty_name}\n\n(Ready in 1 second...)")
        self.status_label.setText("Preparing...")
        self.status_label.setStyleSheet("color: #f9e2af;")

        # Disable detection
        self.detection_enabled = False

        # Start countdown
        try:
            self.ready_timer.timeout.disconnect()
        except TypeError:
            pass # Not connected

        self.ready_timer.timeout.connect(self.enable_axis_detection)
        self.ready_timer.start(1000)

    def enable_axis_detection(self):
        """Enable axis detection after delay"""
        pretty_name, _ = self.xbox_axes[self.axis_map_index]
        self.instruction_label.setText(f"Move or press:\n{pretty_name}\n\n✓ Ready! Move now.")
        self.status_label.setText("Waiting for movement...")
        self.detection_enabled = True
        self.logic.baseline_data = None
        self.last_detection_time = 0

    def start_button_mapping(self):
        """Begin the button mapping process"""
        self.waiting_for_input = True
        self.button_map_index = 0
        self.skip_btn.show()
        self.action_btn.hide()
        self.timer.start(16)
        self.next_button_mapping()

    def next_button_mapping(self):
        """Show next button to map"""
        # Stop any pending timer
        self.ready_timer.stop()

        if self.button_map_index >= len(self.xbox_buttons):
            # Done with buttons
            self.timer.stop()
            self.skip_btn.hide()
            self.action_btn.show()
            self.status_label.setText("✓ Button mapping complete!")
            self.status_label.setStyleSheet("color: #a6e3a1;")
            self.log(f"✓ Mapped {len(self.button_mappings)} buttons")

            # Advance to finish
            self.step += 1
            QTimer.singleShot(1500, self.show_current_step)
            return

        btn_name = self.xbox_buttons[self.button_map_index]
        self.current_target = btn_name

        self.instruction_label.setText(f"Press button:\n{btn_name}\n\n(Ready in 1 second...)\nRelease all buttons!")
        self.status_label.setText("Preparing...")
        self.status_label.setStyleSheet("color: #f9e2af;")

        # Disable detection
        self.detection_enabled = False

        # Start countdown
        try:
            self.ready_timer.timeout.disconnect()
        except TypeError:
            pass

        self.ready_timer.timeout.connect(self.enable_button_detection)
        self.ready_timer.start(1000)

    def enable_button_detection(self):
        """Enable button detection after delay"""
        btn_name = self.xbox_buttons[self.button_map_index]

        # Capture fresh baseline NOW (when user is presumably NOT pressing anything)
        if self.hid_device:
            try:
                data = self.hid_device.read(64)
                if data:
                    self.logic.baseline_data = bytes(data)
                    # Debug log first few bytes
                    hex_str = ' '.join(f'{b:02x}' for b in data[:8])
                    # self.log(f"Baseline: [{hex_str}...]")
            except Exception as e:
                self.log(f"Baseline error: {e}")

        self.instruction_label.setText(f"Press button:\n{btn_name}\n\n(Don't move sticks!)\n✓ Ready! Press now.")
        self.status_label.setText("Waiting for button press...")
        self.detection_enabled = True
        self.last_detection_time = 0

    def process_input(self):
        """Process controller input"""
        if not self.hid_device:
            return

        try:
            data = self.hid_device.read(64)
            if not data:
                return

            if self.step == 0:
                # Axis calibration (always enabled during this step)
                self.logic.process_axis_calibration(data)

            elif self.step == 1 and self.waiting_for_input:
                # Axis mapping

                # Must be enabled (after delay)
                if not self.detection_enabled:
                    return

                # Get all axis bytes we've detected
                excluded = {cfg['offset'] for cfg in self.mapped_axes.values()}

                result = self.logic.detect_axis_movement(data, self.axes_config, excluded)
                if result:
                    byte_index, value = result

                    # Check if already mapped
                    if byte_index in excluded:
                        return

                    # Map it
                    stats = self.axes_config[byte_index]
                    self.mapped_axes[self.current_target] = {
                        'offset': byte_index,
                        'min': stats['min'],
                        'max': stats['max'],
                        'center': stats['center'],
                        'deadzone': stats['deadzone']
                    }

                    pretty_name, _ = self.xbox_axes[self.axis_map_index]
                    self.log(f"✓ {pretty_name} → Byte {byte_index}")
                    self.status_label.setText(f"✓ Detected!")
                    self.status_label.setStyleSheet("color: #a6e3a1;")

                    # Disable detection immediately to prevent double-mapping
                    self.detection_enabled = False

                    self.axis_map_index += 1
                    QTimer.singleShot(800, self.next_axis_mapping)

            elif self.step == 2 and self.waiting_for_input:
                # Button mapping

                # Must be enabled (after delay)
                if not self.detection_enabled:
                    return

                # Get all mapped axis bytes to exclude
                mapped_axis_bytes = {cfg['offset'] for cfg in self.mapped_axes.values()}

                result = self.logic.detect_button(data, self.axes_config, mapped_axis_bytes)
                if result:
                    byte_index, value = result

                    # Map it
                    self.button_mappings[self.current_target] = [byte_index, value]

                    btn_name = self.xbox_buttons[self.button_map_index]
                    self.log(f"✓ {btn_name} → Byte {byte_index} = {value:02x}")
                    self.status_label.setText(f"✓ Detected!")
                    self.status_label.setStyleSheet("color: #a6e3a1;")

                    # Disable detection immediately
                    self.detection_enabled = False

                    self.button_map_index += 1
                    QTimer.singleShot(800, self.next_button_mapping)

        except Exception as e:
            self.log(f"✗ Error: {e}")

    def finish_calibration(self):
        """Save configuration and finish"""
        self.timer.stop()
        self.ready_timer.stop()
        if self.hid_device:
            self.hid_device.close()

        self.step_title.setText("✓ Calibration Complete!")
        self.step_title.setStyleSheet("color: #a6e3a1;")
        self.instruction_label.setText(
            f"Successfully configured:\n"
            f"• {len(self.mapped_axes)} axes\n"
            f"• {len(self.button_mappings)} buttons\n\n"
            f"Click Finish to save."
        )
        self.status_label.setText("")
        self.action_btn.setText("✓ Finish")
        self.skip_btn.hide()
        self.cancel_btn.hide()
        self.action_btn.clicked.disconnect()
        self.action_btn.clicked.connect(self.save_and_close)

    def save_and_close(self):
        """Save configuration and close dialog"""
        config = {
            'device_id': str(self.current_device),
            'mappings': {
                'axes': self.mapped_axes,
            },
            'button_map': self.button_mappings
        }

        self.device_manager.save_device_config(self.current_device, config)
        self.log("✓ Configuration saved!")

        QTimer.singleShot(500, self.accept)

    def log(self, msg):
        """Add message to activity log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.append(f"[{timestamp}] {msg}")
        # Auto-scroll to bottom
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
