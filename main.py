#!/usr/bin/env python3
"""
CloudPad - Main macOS Application
Universal Controller to Xbox Emulator
"""
import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import CloudPadWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("CloudPad")
    
    window = CloudPadWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
