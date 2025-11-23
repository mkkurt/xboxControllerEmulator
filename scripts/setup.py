"""
setup.py for macOS app bundle creation using py2app
Build command: python setup.py py2app
"""

from setuptools import setup
import os

APP = ['cloudpad.py']
DATA_FILES = [
    ('extension', [
        'extension/manifest.json', 
        'extension/content.js',
        'extension/background.js', 
        'extension/popup.html', 
        'extension/popup.js'
    ]),
]

OPTIONS = {
    'argv_emulation': False,
    'packages': [
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui', 
        'PyQt6.QtWidgets',
        'hid',
        'websockets',
        'asyncio',
        'json',
        'threading',
    ],
    'includes': [
        'device_manager',
        'universal_reader',
        'browser_bridge',
        'license_validator'
    ],
    'excludes': [
        'matplotlib',
        'numpy',
        'scipy',
        'PyQt5',
        'tkinter',
    ],
    'resources': [],
    'iconfile': 'resources/icon.icns' if os.path.exists('resources/icon.icns') else None,
    'plist': {
        'CFBundleName': 'CloudPad',
        'CFBundleDisplayName': 'CloudPad',
        'CFBundleIdentifier': 'com.yourname.cloudpad',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
        'LSMinimumSystemVersion': '10.13',
        'NSHumanReadableCopyright': 'Copyright © 2024',
        'NSHighResolutionCapable': True,
        'LSApplicationCategoryType': 'public.app-category.utilities',
    },
    'frameworks': [],
    'site_packages': True,
}

setup(
    name='CloudPad',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
