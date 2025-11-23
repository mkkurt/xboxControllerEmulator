import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QTextEdit, 
    QGroupBox, QProgressBar, QMessageBox, QDialogButtonBox,
    QLineEdit, QFormLayout, QDialog
)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QThread
from PyQt6.QtGui import QFont

from device_manager import DeviceManager
from universal_reader import UniversalInputReader
from browser_bridge import BrowserBridge
from license_validator import LicenseValidator
from ui.theme import Theme
from ui.test_dialog import TestDialog
from ui.input_config_dialog import InputConfigDialog
from ui.calibration_dialog_new import SimpleCalibrationDialog
from build_config import STORE_BUILD

class InputThread(QThread):
    """Thread to handle input reading"""
    state_updated = pyqtSignal(dict)
    
    def __init__(self, reader):
        super().__init__()
        self.reader = reader
        self.running = False
    
    def run(self):
        self.running = True
        while self.running:
            state = self.reader.get_state()
            self.state_updated.emit(state)
            self.msleep(16)  # ~60 FPS
    
    def stop(self):
        self.running = False

class CloudPadWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Setup config directory
        self.config_dir = os.path.expanduser("~/Library/Application Support/CloudPad")
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            
        # Initialize device manager
        self.device_manager = DeviceManager(self.config_dir)
        
        # Initialize input reader
        self.reader = UniversalInputReader(self.device_manager)
        self.bridge = None
        self.license_validator = LicenseValidator(self.config_dir)
        self.input_thread = None
        
        self.init_ui()
        self.scan_devices()
        
        # Auto-refresh devices
        self.device_timer = QTimer()
        self.device_timer.timeout.connect(self.scan_devices)
        self.device_timer.start(2000)  # Every 2 seconds
    
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("CloudPad - Universal Controller Emulator")
        self.setGeometry(100, 100, 1000, 700)
        
        # Modern styling
        self.setStyleSheet(Theme.get_stylesheet())
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        
        # Main layout
        main_layout = QVBoxLayout(central)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("🎮 CloudPad")
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #89b4fa; margin-bottom: 4px;")
        main_layout.addWidget(title)
        
        subtitle = QLabel("Universal Controller Emulator for Cloud Gaming")
        subtitle.setFont(QFont("Arial", 12))
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #a6adc8; margin-bottom: 16px;")
        main_layout.addWidget(subtitle)
        
        # Content layout (side by side)
        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)
        
        # Left panel - Devices
        left_panel = self.create_device_panel()
        content_layout.addWidget(left_panel)
        
        # Right panel - Status
        right_panel = self.create_status_panel()
        content_layout.addWidget(right_panel)
        
        # Bottom controls
        controls_layout = QHBoxLayout()
        main_layout.addLayout(controls_layout)
        
        self.start_btn = QPushButton("▶ Start Emulation")
        self.start_btn.setMinimumHeight(50)
        self.start_btn.setStyleSheet("QPushButton { font-size: 16px; font-weight: bold; }")
        self.start_btn.clicked.connect(self.toggle_emulation)
        controls_layout.addWidget(self.start_btn)
        
        self.calibrate_btn = QPushButton("⚙ Auto-Calibrate")
        self.calibrate_btn.setMinimumHeight(50)
        self.calibrate_btn.clicked.connect(self.run_calibration)
        controls_layout.addWidget(self.calibrate_btn)
        
        extension_btn = QPushButton("🌐 Browser Extension")
        extension_btn.setMinimumHeight(50)
        extension_btn.setStyleSheet("QPushButton { background-color: #f38ba8; } QPushButton:hover { background-color: #f5c2e7; }")
        extension_btn.clicked.connect(self.show_extension_dialog)
        controls_layout.addWidget(extension_btn)
        
        config_btn = QPushButton("🎛 Configure")
        config_btn.setMinimumHeight(50)
        config_btn.clicked.connect(self.configure_input)
        controls_layout.addWidget(config_btn)
        
        test_btn = QPushButton("🎮 Test Input")
        test_btn.setMinimumHeight(50)
        test_btn.clicked.connect(self.test_input)
        controls_layout.addWidget(test_btn)
        
        # Only show license button for Direct builds
        if not STORE_BUILD:
            license_btn = QPushButton("🔑 License")
            license_btn.setMinimumHeight(50)
            license_btn.clicked.connect(self.show_license_dialog)
            controls_layout.addWidget(license_btn)
        
        update_btn = QPushButton("⬇ Check Updates")
        update_btn.clicked.connect(self.check_updates)
        controls_layout.addWidget(update_btn)
        
        # Status bar
        self.update_license_status()
        self.statusBar().showMessage("Ready")
        
        # Check first run after a short delay to allow window to show
        QTimer.singleShot(1000, self.check_first_run)
    
    def create_device_panel(self):
        """Create the device list panel"""
        group = QGroupBox("Connected Devices")
        layout = QVBoxLayout()
        
        self.device_list = QListWidget()
        self.device_list.itemSelectionChanged.connect(self.on_device_selected)
        layout.addWidget(self.device_list)
        
        refresh_btn = QPushButton("🔄 Refresh")
        refresh_btn.clicked.connect(self.scan_devices)
        layout.addWidget(refresh_btn)
        
        group.setLayout(layout)
        return group
    
    def create_status_panel(self):
        """Create the status/log panel"""
        group = QGroupBox("Status")
        layout = QVBoxLayout()
        
        # Connection status
        self.connection_label = QLabel("Status: Not Running")
        self.connection_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(self.connection_label)
        
        # Activity indicator
        self.activity_bar = QProgressBar()
        self.activity_bar.setMaximum(100)
        self.activity_bar.setValue(0)
        self.activity_bar.setTextVisible(False)
        layout.addWidget(self.activity_bar)
        
        # Log output
        log_label = QLabel("Activity Log:")
        layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        layout.addWidget(self.log_text)
        
        group.setLayout(layout)
        return group
    
    def scan_devices(self):
        """Scan for connected devices"""
        devices = self.device_manager.scan_devices()
        
        # Check if devices changed to avoid unnecessary redraws
        current_uids = {d.uid for d in devices}
        displayed_uids = set()
        for i in range(self.device_list.count()):
            item_text = self.device_list.item(i).text()
            try:
                # Extract UID from "✓ Name (VID:PID)"
                uid = item_text.split('(')[1].split(')')[0]
                displayed_uids.add(uid)
            except:
                pass
                
        # If sets match, no change needed (unless config status changed, but that's rare)
        if current_uids == displayed_uids and self.device_list.count() == len(devices):
            return

        # Store current selection
        selected_uid = None
        if self.device_list.selectedItems():
            try:
                text = self.device_list.selectedItems()[0].text()
                selected_uid = text.split('(')[1].split(')')[0]
            except:
                pass

        self.device_list.clear()
        
        for device in devices:
            config = self.device_manager.get_device_config(device)
            status = "✓" if config else "✗"
            item_text = f"{status} {device}"
            self.device_list.addItem(item_text)
            
            # Restore selection
            if selected_uid and device.uid == selected_uid:
                self.device_list.setCurrentRow(self.device_list.count() - 1)
        
        if not devices:
            self.device_list.addItem("No devices detected")
        
        self.log(f"Scanned: Found {len(devices)} device(s)")
    
    def on_device_selected(self):
        """Handle device selection"""
        pass
    
    def toggle_emulation(self):
        """Start or stop emulation"""
        if self.bridge and self.bridge.running:
            self.stop_emulation()
        else:
            self.start_emulation()
    
    def start_emulation(self):
        """Start the emulation"""
        # Start reader
        if not self.reader.start():
            QMessageBox.warning(self, "Error", "No configured devices found!\n\nPlease calibrate a device first.")
            return
        
        self.log("Started input reader")
        
        # Start browser bridge
        self.bridge = BrowserBridge()
        self.bridge.start()
        self.log("Started browser bridge on ws://127.0.0.1:8765")
        
        # Start input thread
        self.input_thread = InputThread(self.reader)
        self.input_thread.state_updated.connect(self.on_state_update)
        self.input_thread.start()
        
        # Update UI
        self.start_btn.setText("⏹ Stop Emulation")
        self.start_btn.setStyleSheet("QPushButton { background-color: #ff4444; font-size: 16px; font-weight: bold; }")
        self.connection_label.setText("Status: Running - Waiting for browser connection")
        self.connection_label.setStyleSheet("font-size: 14px; font-weight: bold; color: green;")
        self.statusBar().showMessage("Emulation active - Connect browser to ws://127.0.0.1:8765")
        self.log("✓ Emulation started!")
    
    def stop_emulation(self):
        """Stop the emulation"""
        if self.input_thread:
            self.input_thread.stop()
            self.input_thread.wait()
            self.input_thread = None
        
        if self.bridge:
            self.bridge.stop()
            self.bridge = None
        
        self.reader.stop()
        self.start_btn.setText("▶ Start Emulation")
        self.start_btn.setStyleSheet("QPushButton { background-color: transparent; font-size: 16px; font-weight: bold; }")
        self.connection_label.setText("Status: Stopped")
        self.connection_label.setStyleSheet("font-size: 14px; font-weight: bold; color: gray;")
        self.statusBar().showMessage("Ready")
        self.log("Emulation stopped")
    
    def configure_input(self):
        """Open advanced input configuration"""
        items = self.device_list.selectedItems()
        if not items:
            QMessageBox.warning(self, "Select Device", "Please select a device to configure.")
            return
            
        # Parse selection to find device
        # Format: "✓ Name (VID:PID)"
        text = items[0].text()
        try:
            uid = text.split('(')[1].split(')')[0]
        except IndexError:
            QMessageBox.warning(self, "Error", "Could not parse device ID.")
            return
        
        # Find device object
        target_device = None
        for device in self.device_manager.devices:
            if device.uid == uid:
                target_device = device
                break
        
        if target_device:
            dialog = InputConfigDialog(self.device_manager, target_device, self)
            dialog.exec()
        else:
            QMessageBox.warning(self, "Error", "Device not found!")

    def test_input(self):
        """Open controller tester"""
        self.test_dialog = TestDialog(self)
        
        # Ensure input reading is active
        was_running = self.input_thread is not None
        if not was_running:
            self.start_emulation()
            
        self.test_dialog.exec()
        self.test_dialog = None
        
        if not was_running:
            self.stop_emulation()

    def check_first_run(self):
        """Check if this is the first run"""
        if not self.device_manager.device_configs:
            QMessageBox.information(
                self,
                "Welcome to CloudPad!",
                "It looks like this is your first time here.\n\n"
                "1. Connect your controller 🎮\n"
                "2. Click 'Refresh' to detect it 🔄\n"
                "3. If it's a supported device, it will work automatically!\n"
                "4. If not, click 'Configure' to calibrate it ⚙️"
            )

    def check_updates(self):
        """Check for updates"""
        # In a real app, this would query an API
        # For now, open GitHub releases
        import webbrowser
        webbrowser.open("https://github.com/kutay/cloudpad/releases")

    def on_state_update(self, state):
        """Handle state updates from input thread"""
        # Update activity indicator
        active = len(state) > 0
        self.activity_bar.setValue(100 if active else 0)
        
        # Broadcast to browser
        if self.bridge:
            self.bridge.broadcast(state)
            
        # Update test dialog if open
        if hasattr(self, 'test_dialog') and self.test_dialog:
            self.test_dialog.update_state(state)
    
    def run_calibration(self):
        """Run the calibration wizard"""
        devices = self.device_manager.scan_devices()
        if not devices:
            QMessageBox.warning(self, "No Devices", "No devices detected!\n\nPlease connect a controller.")
            return
        # Run integrated calibration dialog
        try:
            wizard = SimpleCalibrationDialog(self.device_manager, self)
            if wizard.exec():
                self.scan_devices()
                self.log("✓ Calibration completed successfully")
                QMessageBox.information(
                    self,
                    "Success",
                    "Controller calibrated successfully!\n\nYour button mappings have been saved."
                )
            else:
                self.log("Calibration cancelled")
                
        except Exception as e:
            self.log(f"Calibration error: {e}")
            QMessageBox.critical(self, "Error", f"Calibration failed:\n\n{str(e)}")
    
    def show_extension_dialog(self):
        """Show browser extension installation instructions"""
        from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel, QGroupBox
        from PyQt6.QtGui import QFont
        from PyQt6.QtCore import Qt
        import os
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Browser Extension - CloudPad")
        dialog.setMinimumWidth(600)
        dialog.setStyleSheet("QDialog { background-color: #1e1e2e; }")
        
        layout = QVBoxLayout()
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        
        # Title
        title_label = QLabel("🌐 CloudPad Browser Extension")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #f38ba8; margin-bottom: 8px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel(
            "Required for cloud gaming platforms to recognize your controller"
        )
        desc_label.setFont(QFont("Arial", 11))
        desc_label.setStyleSheet("color: #a6adc8; margin-bottom: 16px;")
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        # Supported platforms box
        platforms_box = QGroupBox("✓ Supported Platforms")
        platforms_box.setStyleSheet("""
            QGroupBox {
                background-color: #181825;
                border: 2px solid #313244;
                border-radius: 8px;
                padding: 16px;
                margin-top: 8px;
            }
            QGroupBox::title {
                color: #a6e3a1;
                font-weight: bold;
            }
        """)
        platforms_layout = QVBoxLayout()
        platforms_text = QLabel(
            "• Xbox Cloud Gaming (xbox.com)\n"
            "• GeForce NOW (geforcenow.com)\n"
            "• Amazon Luna (amazon.com/luna)"
        )
        platforms_text.setStyleSheet("color: #cdd6f4; line-height: 1.6;")
        platforms_layout.addWidget(platforms_text)
        platforms_box.setLayout(platforms_layout)
        layout.addWidget(platforms_box)
        
        # Installation steps
        steps_label = QLabel("📋 <b>Installation Steps:</b>")
        steps_label.setFont(QFont("Arial", 13, QFont.Weight.Bold))
        steps_label.setStyleSheet("color: #89b4fa; margin-top: 16px; margin-bottom: 8px;")
        layout.addWidget(steps_label)
        
        steps_text = QLabel(
            "<ol style='line-height: 1.8; margin-left: -20px;'>"
            "<li>Click the button below to open the extension folder</li>"
            "<li>Open Chrome → go to <b>chrome://extensions/</b></li>"
            "<li>Enable <b>Developer mode</b> (toggle in top-right)</li>"
            "<li>Click <b>Load unpacked</b></li>"
            "<li>Select the 'extension' folder that was opened</li>"
            "<li>Done! The extension is now installed</li>"
            "</ol>"
        )
        steps_text.setWordWrap(True)
        steps_text.setStyleSheet("""
            color: #cdd6f4;
            background-color: #181825;
            padding: 16px;
            border-radius: 8px;
            border: 1px solid #313244;
        """)
        layout.addWidget(steps_text)
        
        # Open folder button
        open_btn = QPushButton("📁 Open Extension Folder")
        open_btn.setMinimumHeight(45)
        open_btn.setStyleSheet("""
            QPushButton {
                background-color: #a6e3a1;
                color: #1e1e2e;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #94e2d5;
            }
        """)
        # Fix path to extension folder
        ext_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "extension")
        open_btn.clicked.connect(lambda: self.open_extension_folder(ext_path))
        layout.addWidget(open_btn)
        
        # Note
        note_label = QLabel(
            "💡 <i>After installation, restart CloudPad and your browser for changes to take effect.</i>"
        )
        note_label.setWordWrap(True)
        note_label.setStyleSheet("color: #f9e2af; margin-top: 12px; font-size: 11px;")
        layout.addWidget(note_label)
        
        # Close button
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.setStyleSheet("QPushButton { min-width: 80px; }")
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def open_extension_folder(self, path):
        """Open extension folder in Finder"""
        import subprocess
        if os.path.exists(path):
            subprocess.run(["open", path])
            self.log(f"Opened extension folder: {path}")
        else:
            QMessageBox.warning(self, "Folder Not Found", f"Extension folder not found at:\n{path}")
    
    def update_license_status(self):
        """Update UI based on license tier"""
        info = self.license_validator.get_license_info()
        tier = info.get('tier', 'free').upper()
        
        if tier == 'PRO':
            self.statusBar().showMessage(f"CloudPad Pro • License: {info.get('key', 'N/A')[:9]}...")
        else:
            self.statusBar().showMessage("CloudPad Free • Single device limit")
    
    def show_license_dialog(self):
        """Show license activation dialog"""
        from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QLineEdit, QFormLayout
        from PyQt6.QtGui import QFont
        from PyQt6.QtWidgets import QVBoxLayout, QLabel
        
        dialog = QDialog(self)
        dialog.setWindowTitle("CloudPad License")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Current status
        info = self.license_validator.get_license_info()
        tier = info.get('tier', 'free').upper()
        
        status_label = QLabel(f"Current Tier: {tier}")
        status_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(status_label)
        
        if tier == 'FREE':
            # Upgrade section
            upgrade_label = QLabel(
                "Upgrade to Pro ($14.99) for:\n"
                "• Unlimited devices\n"
                "• Advanced mapping features\n"
                "• Macro support\n"
                "• Axis curves & deadzones\n"
                "• Priority support"
            )
            layout.addWidget(upgrade_label)
            
            # License key input
            form = QFormLayout()
            key_input = QLineEdit()
            key_input.setPlaceholderText("XXXX-XXXX-XXXX-XXXX")
            form.addRow("License Key:", key_input)
            
            email_input = QLineEdit()
            email_input.setPlaceholderText("your@email.com (optional)")
            form.addRow("Email:", email_input)
            
            layout.addLayout(form)
            
            # Buttons
            button_box = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Ok | 
                QDialogButtonBox.StandardButton.Cancel
            )
            button_box.accepted.connect(lambda: self.activate_license(key_input.text(), email_input.text(), dialog))
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)
        else:
            # Pro user info
            key_label = QLabel(f"License Key: {info.get('key', 'N/A')}")
            layout.addWidget(key_label)
            
            activated_label = QLabel(f"Activated: {info.get('activated_at', 'N/A')[:10]}")
            layout.addWidget(activated_label)
            
            # Close button
            button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)
        
        dialog.setLayout(layout)
        dialog.exec()
    
    def activate_license(self, key, email, dialog):
        """Activate license key"""
        if self.license_validator.activate_license(key, email):
            QMessageBox.information(self, "Success", "License activated successfully!\n\nPlease restart CloudPad for changes to take effect.")
            self.update_license_status()
            dialog.accept()
        else:
            QMessageBox.warning(self, "Invalid License", "The license key you entered is invalid.\n\nPlease check and try again.")
    
    def log(self, message):
        """Add message to log"""
        self.log_text.append(f"• {message}")
    
    def closeEvent(self, event):
        """Handle window close"""
        if self.bridge and self.bridge.running:
            self.stop_emulation()
        event.accept()
