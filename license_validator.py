#!/usr/bin/env python3
"""
License Validation System for CloudPad
Supports offline validation with online verification
"""
import hashlib
import json
import os
from datetime import datetime, timedelta
from typing import Optional, Dict

import requests
from build_config import STORE_BUILD

class LicenseValidator:
    def __init__(self, config_dir="."):
        self.config_dir = config_dir
        self.license_file = os.path.join(config_dir, "license.json")
        self._cached_license = None
        
    def validate_license_key(self, license_key: str) -> bool:
        """
        Validate license key format
        """
        if not license_key:
            return False
        return True # We let the API decide validity
    
    def verify_online(self, license_key: str) -> bool:
        """Verify key with Gumroad API"""
        try:
            response = requests.post(
                "https://api.gumroad.com/v2/licenses/verify",
                data={
                    "product_permalink": "cloudpad", # Replace with actual permalink
                    "license_key": license_key
                },
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('success', False) and not data.get('purchase', {}).get('refunded', False)
            return False
        except Exception as e:
            print(f"Validation error: {e}")
            # Fallback: If network fails, trust the key if it looks valid?
            # For strict security, return False. For UX, maybe True if previously validated.
            return False

    def activate_license(self, license_key: str, email: str = "") -> bool:
        """Activate a license key"""
        # Online check
        if not self.verify_online(license_key):
            return False
        
        license_data = {
            'key': license_key,
            'email': email,
            'activated_at': datetime.now().isoformat(),
            'tier': 'pro',
            'last_verified': datetime.now().isoformat()
        }
        
        try:
            with open(self.license_file, 'w') as f:
                json.dump(license_data, f, indent=2)
            self._cached_license = license_data
            return True
        except Exception as e:
            print(f"Error saving license: {e}")
            return False
    
    def get_license_info(self) -> Dict:
        """Get current license information"""
        if STORE_BUILD:
            return {'tier': 'pro', 'key': 'App Store License'}

        if self._cached_license:
            return self._cached_license
        
        if os.path.exists(self.license_file):
            try:
                with open(self.license_file, 'r') as f:
                    self._cached_license = json.load(f)
                return self._cached_license
            except:
                pass
        
        return {'tier': 'free', 'key': None}
    
    def is_pro(self) -> bool:
        """Check if user has Pro license"""
        if STORE_BUILD:
            return True
            
        info = self.get_license_info()
        return info.get('tier') == 'pro'
    
    def deactivate_license(self):
        """Remove license (for testing/uninstall)"""
        if os.path.exists(self.license_file):
            os.remove(self.license_file)
        self._cached_license = None
    
    def get_tier_features(self) -> Dict:
        """Get features available for current tier"""
        is_pro = self.is_pro()

        return {
            'max_devices': None if is_pro else 1,
            'profiles': is_pro,
            'advanced_mapping': is_pro,
            'macros': is_pro,
            'curves': is_pro,
            'priority_support': is_pro
        }

    def _calculate_checksum(self, data: str) -> str:
        """Calculate a simple checksum for license key validation"""
        checksum = 0
        for char in data:
            checksum ^= ord(char)
        return f"{checksum:04X}"

# CLI for testing
def main():
    import sys
    
    validator = LicenseValidator()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 license_validator.py check")
        print("  python3 license_validator.py activate <KEY>")
        print("  python3 license_validator.py deactivate")
        print("  python3 license_validator.py generate <TEXT>")
        return
    
    command = sys.argv[1]
    
    if command == "check":
        info = validator.get_license_info()
        print(f"Tier: {info.get('tier', 'free').upper()}")
        if info.get('key'):
            print(f"License: {info['key']}")
            print(f"Email: {info.get('email', 'N/A')}")
        
        features = validator.get_tier_features()
        print("\nFeatures:")
        for feature, enabled in features.items():
            status = "✓" if enabled else "✗"
            print(f"  {status} {feature}: {enabled}")
    
    elif command == "activate":
        if len(sys.argv) < 3:
            print("Error: License key required")
            return
        
        key = sys.argv[2]
        email = sys.argv[3] if len(sys.argv) > 3 else ""
        
        if validator.activate_license(key, email):
            print(f"✓ License activated successfully!")
            print(f"Key: {key}")
            print(f"Tier: PRO")
        else:
            print("✗ Invalid license key")
    
    elif command == "deactivate":
        validator.deactivate_license()
        print("License deactivated")
    
    elif command == "generate":
        # Generate a valid license key from text (for testing)
        if len(sys.argv) < 3:
            print("Error: Text required")
            return
        
        text = sys.argv[2]
        # Use first 12 chars of hash
        hash_obj = hashlib.sha256(text.encode())
        key_data = hash_obj.hexdigest()[:12].upper()
        checksum = validator._calculate_checksum(key_data)
        
        formatted_key = f"{key_data[:4]}-{key_data[4:8]}-{key_data[8:12]}-{checksum}"
        print(f"Generated license key: {formatted_key}")
        print(f"(This is for TESTING only)")

if __name__ == "__main__":
    main()
