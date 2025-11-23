#!/usr/bin/env python3
"""
Device Manager - Universal HID Controller Detection and Configuration
Supports any HID device (joysticks, HOTAS, racing wheels, gamepads)
"""
import hid
import json
import os
from typing import List, Dict, Optional

class DeviceInfo:
    def __init__(self, vendor_id: int, product_id: int, manufacturer: str, product: str, path: bytes):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.manufacturer = manufacturer or "Unknown"
        self.product = product or "Unknown Device"
        self.path = path
        self.uid = f"{vendor_id:04x}:{product_id:04x}"
    
    def __repr__(self):
        return f"{self.manufacturer} {self.product} ({self.uid})"

class DeviceManager:
    def __init__(self, config_dir="."):
        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, "devices.json")
        self.devices: List[DeviceInfo] = []
        self.device_configs: Dict[str, dict] = {}
        self.preset_cache: Dict[str, dict] = {}
        self.load_device_configs()
        self._load_presets()
    
    def scan_devices(self) -> List[DeviceInfo]:
        """Scan for all connected HID devices"""
        self.devices = []
        
        for device_dict in hid.enumerate():
            # Filter out non-controller devices (keyboards, mice, etc.)
            # Most game controllers have usage_page 1 (Generic Desktop)
            usage_page = device_dict.get('usage_page', 0)
            usage = device_dict.get('usage', 0)
            
            # Common controller usage values:
            # Usage 4 = Joystick, Usage 5 = Gamepad, Usage 8 = Multi-axis Controller
            if usage_page == 1 and usage in [4, 5, 8]:
                device_info = DeviceInfo(
                    vendor_id=device_dict['vendor_id'],
                    product_id=device_dict['product_id'],
                    manufacturer=device_dict.get('manufacturer_string'),
                    product=device_dict.get('product_string'),
                    path=device_dict['path']
                )
                self.devices.append(device_info)
        
        return self.devices
    
    def get_device_config(self, device: DeviceInfo) -> Optional[dict]:
        """Get configuration for a device, checking presets if no user config exists"""
        # 1. Check user config
        if device.uid in self.device_configs:
            return self.device_configs[device.uid]
            
        # 2. Check presets (cached)
        return self._find_preset(device)
    
    def save_device_config(self, device: DeviceInfo, config: dict):
        """Save configuration for a device"""
        self.device_configs[device.uid] = config
        self._save_configs()
    
    def load_device_configs(self):
        """Load saved configurations"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.device_configs = json.load(f)
            except Exception as e:
                print(f"Error loading configs: {e}")
                self.device_configs = {}

    def _load_presets(self):
        """Load all presets into cache"""
        import sys
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.dirname(__file__)
            
        presets_dir = os.path.join(base_path, 'presets')
        if not os.path.exists(presets_dir):
            return
            
        for filename in os.listdir(presets_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(presets_dir, filename), 'r') as f:
                        preset = json.load(f)
                        # Store by VID:PID if available in preset, or we need a way to match
                        # Current presets don't have VID/PID in filename, but inside json?
                        # Let's assume we scan them when needed or cache them by content?
                        # Actually, _find_preset iterates them. Let's just cache the list of presets.
                        self.preset_cache[filename] = preset
                except Exception as e:
                    print(f"Error loading preset {filename}: {e}")

    def _find_preset(self, device: DeviceInfo) -> Optional[dict]:
        """Search cached presets for matching device"""
        for preset in self.preset_cache.values():
            if preset.get('vendor_id') == device.vendor_id and preset.get('product_id') == device.product_id:
                return preset
        return None
    
    def _save_configs(self):
        """Save configurations to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.device_configs, f, indent=2)
        except Exception as e:
            print(f"Error saving device configs: {e}")
    
    def open_device(self, device: DeviceInfo) -> Optional[hid.device]:
        """Open a HID device for reading"""
        try:
            dev = hid.device()
            dev.open_path(device.path)
            dev.set_nonblocking(True)
            return dev
        except Exception as e:
            print(f"Error opening device {device}: {e}")
            return None

def main():
    """Test device detection"""
    manager = DeviceManager()
    devices = manager.scan_devices()
    
    print("="*60)
    print("DEVICE MANAGER - HID CONTROLLER DETECTION")
    print("="*60)
    print(f"\nFound {len(devices)} controller(s):\n")
    
    for i, device in enumerate(devices):
        print(f"{i+1}. {device}")
        print(f"   UID: {device.uid}")
        print(f"   Path: {device.path}")
        
        # Check if we have config for this device
        config = manager.get_device_config(device)
        if config:
            print(f"   Status: ✓ Configured")
        else:
            print(f"   Status: ✗ Not configured")
        print()
    
    if not devices:
        print("No controllers detected. Please connect your device and try again.")
        return 1
    
    print("="*60)
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
