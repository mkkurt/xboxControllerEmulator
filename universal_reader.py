#!/usr/bin/env python3
"""
Universal Input Reader - Works with any HID device
Automatically learns the structure of HID reports
"""
import threading
import time
from typing import Dict, Optional, List
from device_manager import DeviceManager, DeviceInfo
from input_processor import InputProcessor

class UniversalInputReader:
    def __init__(self, device_manager=None):
        self.device_manager = device_manager or DeviceManager()
        self.active_devices = {}  # uid -> device handle
        self.processors = {}      # uid -> InputProcessor
        self.state = {}  # Combined state from all devices
        self.running = False
        self.lock = threading.Lock()
        self.thread = None
        
        # Raw data from each device
        self.raw_data = {}  # uid -> latest raw bytes
        
    def start(self):
        """Start reading from all configured devices"""
        devices = self.device_manager.scan_devices()
        
        for device in devices:
            handle = self.device_manager.open_device(device)
            if handle:
                config = self.device_manager.get_device_config(device) or {}
                self.active_devices[device.uid] = {
                    'handle': handle,
                    'info': device,
                    'config': config
                }
                
                # Initialize Input Processor
                processor = InputProcessor()
                if 'processing' in config:
                    processor.update_config(config['processing'])
                self.processors[device.uid] = processor
                
                print(f"Connected to: {device}")
        
        if not self.active_devices:
            print("No devices connected!")
            return False
        
        self.running = True
        self.thread = threading.Thread(target=self._read_loop, daemon=True)
        self.thread.start()
        return True
    
    def stop(self):
        """Stop reading and close devices"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        
        for uid, dev_info in self.active_devices.items():
            try:
                dev_info['handle'].close()
            except:
                pass
        
        self.active_devices = {}
    
    def _read_loop(self):
        """Main reading loop"""
        while self.running:
            for uid, dev_info in self.active_devices.items():
                try:
                    data = dev_info['handle'].read(64, timeout_ms=10)
                    if data:
                        self._process_data(uid, data, dev_info['config'])
                except Exception as e:
                    # Non-blocking read, timeout is expected
                    pass
            
            time.sleep(0.001)  # 1ms sleep to avoid burning CPU
    
    def _process_data(self, uid: str, data: List[int], config: dict):
        """Process raw HID data based on device configuration"""
        with self.lock:
            self.raw_data[uid] = data
            
            if not config or 'mappings' not in config:
                # No configuration - store raw data only
                return
            
            # Apply configured mappings
            mappings = config['mappings']
            
            # Process buttons (Legacy format)
            if 'buttons' in mappings:
                button_config = mappings['buttons']
                offset = button_config.get('offset', 1)
                num_bytes = button_config.get('num_bytes', 2)
                
                # Combine button bytes into integer
                buttons = 0
                for i in range(num_bytes):
                    if offset + i < len(data):
                        buttons |= (data[offset + i] << (8 * i))
                
                self.state[f'{uid}_buttons'] = buttons

            # Process buttons (New Calibration format)
            if 'button_map' in config:
                # Format: {'A': [byte_index, value], ...}
                for btn_name, (byte_idx, active_value) in config['button_map'].items():
                    if byte_idx < len(data):
                        # Check if button is pressed (byte value matches active value)
                        # Note: This assumes simple on/off. For bitmasks we might need more logic.
                        # The calibration detects 'new' value. 
                        # If it's a bitmask, we should probably store the mask.
                        # For now, let's assume exact match or bitwise AND if value is power of 2
                        
                        current_val = data[byte_idx]
                        is_pressed = False
                        
                        # Heuristic: if active_value is power of 2, treat as bitmask
                        if active_value > 0 and (active_value & (active_value - 1)) == 0:
                            is_pressed = (current_val & active_value) > 0
                        else:
                            is_pressed = (current_val == active_value)
                            
                        self.state[f'{uid}_btn_{btn_name}'] = is_pressed
            
            # Process axes
            if 'axes' in mappings:
                for axis_name, axis_config in mappings['axes'].items():
                    offset = axis_config['offset']
                    size = axis_config.get('size', 2)
                    min_val = axis_config.get('min', 0)
                    max_val = axis_config.get('max', 65535)
                    invert = axis_config.get('invert', False)
                    
                    # Read multi-byte value (little-endian)
                    raw_value = 0
                    for i in range(size):
                        if offset + i < len(data):
                            raw_value |= (data[offset + i] << (8 * i))
                    
                    # Normalize to -1.0 to 1.0 or 0.0 to 1.0
                    if 'center' in axis_config:
                        center = axis_config['center']
                        if raw_value < center:
                            normalized = (raw_value - min_val) / (center - min_val) - 1.0
                        else:
                            normalized = (raw_value - center) / (max_val - center)
                    else:
                        normalized = (raw_value - min_val) / (max_val - min_val)
                    
                    if invert:
                        normalized = -normalized if 'center' in axis_config else 1.0 - normalized
                    
                    # Clamp
                    normalized = max(-1.0, min(1.0, normalized))
                    
                    # Apply Advanced Processing (Deadzones, Curves, Smoothing)
                    if uid in self.processors:
                        normalized = self.processors[uid].process_axis(axis_name, normalized)
                    
                    self.state[f'{uid}_{axis_name}'] = normalized
            
            # Process hat/dpad
            if 'hat' in mappings:
                hat_config = mappings['hat']
                offset = hat_config['offset']
                if offset < len(data):
                    hat_raw = data[offset]
                    hat_dir = (hat_raw >> 4) & 0x0F
                    self.state[f'{uid}_hat'] = hat_dir if hat_dir < 8 else -1
    
    def get_state(self) -> dict:
        """Get current state of all devices"""
        with self.lock:
            return self.state.copy()
    
    def get_raw_data(self, uid: str) -> Optional[List[int]]:
        """Get raw HID data for a specific device"""
        with self.lock:
            return self.raw_data.get(uid)

# Test code
if __name__ == "__main__":
    reader = UniversalInputReader()
    
    if not reader.start():
        print("Failed to start!")
        exit(1)
    
    print("\nReading input... (Press Ctrl+C to stop)\n")
    
    try:
        while True:
            state = reader.get_state()
            
            # Print raw data from all devices
            for uid in reader.active_devices.keys():
                raw = reader.get_raw_data(uid)
                if raw:
                    print(f"{uid}: {[hex(x) for x in raw[:16]]}")
            
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping...")
    
    reader.stop()
