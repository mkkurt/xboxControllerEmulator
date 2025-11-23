"""
CloudPad Premium Theme
Defines the color palette and stylesheets for the application.
"""

class Theme:
    # Catppuccin Mocha Palette
    BASE = "#1e1e2e"
    MANTLE = "#181825"
    CRUST = "#11111b"
    
    TEXT = "#cdd6f4"
    SUBTEXT0 = "#a6adc8"
    SUBTEXT1 = "#bac2de"
    
    BLUE = "#89b4fa"
    LAVENDER = "#b4befe"
    SAPPHIRE = "#74c7ec"
    SKY = "#89dceb"
    
    RED = "#f38ba8"
    MAROON = "#eba0ac"
    PEACH = "#fab387"
    YELLOW = "#f9e2af"
    GREEN = "#a6e3a1"
    TEAL = "#94e2d5"
    
    OVERLAY0 = "#6c7086"
    OVERLAY1 = "#7f849c"
    OVERLAY2 = "#9399b2"
    
    SURFACE0 = "#313244"
    SURFACE1 = "#45475a"
    SURFACE2 = "#585b70"
    
    @classmethod
    def get_stylesheet(cls):
        return f"""
            QMainWindow {{
                background-color: {cls.BASE};
            }}
            QWidget {{
                background-color: {cls.BASE};
                color: {cls.TEXT};
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                font-size: 13px;
            }}
            
            /* Group Boxes */
            QGroupBox {{
                border: 1px solid {cls.SURFACE0};
                border-radius: 8px;
                margin-top: 24px;
                padding-top: 16px;
                font-weight: 600;
                color: {cls.BLUE};
                background-color: {cls.MANTLE};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 12px;
                padding: 0 4px;
                background-color: {cls.BASE};
            }}
            
            /* Buttons */
            QPushButton {{
                background-color: {cls.SURFACE0};
                color: {cls.TEXT};
                border: 1px solid {cls.SURFACE1};
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background-color: {cls.SURFACE1};
                border-color: {cls.SURFACE2};
            }}
            QPushButton:pressed {{
                background-color: {cls.SURFACE2};
            }}
            QPushButton[class="primary"] {{
                background-color: {cls.BLUE};
                color: {cls.BASE};
                border: none;
            }}
            QPushButton[class="primary"]:hover {{
                background-color: {cls.LAVENDER};
            }}
            QPushButton[class="danger"] {{
                background-color: {cls.RED};
                color: {cls.BASE};
                border: none;
            }}
            QPushButton[class="danger"]:hover {{
                background-color: {cls.MAROON};
            }}
            
            /* Inputs */
            QLineEdit, QTextEdit, QPlainTextEdit {{
                background-color: {cls.CRUST};
                border: 1px solid {cls.SURFACE0};
                border-radius: 4px;
                padding: 8px;
                color: {cls.TEXT};
                selection-background-color: {cls.SURFACE2};
            }}
            QLineEdit:focus, QTextEdit:focus {{
                border: 1px solid {cls.BLUE};
            }}
            
            /* Lists & Trees */
            QListWidget, QTreeWidget {{
                background-color: {cls.MANTLE};
                border: 1px solid {cls.SURFACE0};
                border-radius: 6px;
                outline: none;
            }}
            QListWidget::item {{
                padding: 8px;
                border-radius: 4px;
            }}
            QListWidget::item:selected {{
                background-color: {cls.SURFACE1};
                color: {cls.TEXT};
            }}
            QListWidget::item:hover {{
                background-color: {cls.SURFACE0};
            }}
            
            /* Scrollbars */
            QScrollBar:vertical {{
                border: none;
                background: {cls.MANTLE};
                width: 10px;
                margin: 0;
            }}
            QScrollBar::handle:vertical {{
                background: {cls.SURFACE0};
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {cls.SURFACE1};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            
            /* Sliders */
            QSlider::groove:horizontal {{
                border: 1px solid {cls.SURFACE0};
                height: 6px;
                background: {cls.CRUST};
                margin: 2px 0;
                border-radius: 3px;
            }}
            QSlider::handle:horizontal {{
                background: {cls.BLUE};
                border: 1px solid {cls.BLUE};
                width: 16px;
                height: 16px;
                margin: -6px 0;
                border-radius: 8px;
            }}
            QSlider::handle:horizontal:hover {{
                background: {cls.LAVENDER};
            }}
        """
