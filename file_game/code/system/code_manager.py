"""Code manager for handling redeem codes"""

import json
import os
from pathlib import Path
from datetime import datetime


class CodeManager:
    """Manages redeem codes and their usage"""
    
    def __init__(self, codes_file: str = "file_game/json/codes.json", used_codes_file: str = "file_game/json/used_codes.json"):
        """
        Initialize the code manager
        
        Args:
            codes_file: Path to file containing available codes
            used_codes_file: Path to file tracking used codes
        """
        self.codes_file = codes_file
        self.used_codes_file = used_codes_file
        self.available_codes = {}
        self.used_codes = set()
        
        # Load codes
        self._load_codes()
        self._load_used_codes()
        
        # Initialize default codes if none exist
        if not self.available_codes:
            self._initialize_default_codes()
    
    def _initialize_default_codes(self):
        """Initialize some default redeem codes"""
        default_codes = {
            "WELCOME2024": {"coins": 500, "description": "Welcome bonus"},
            "HERO100": {"coins": 100, "description": "Starter pack"},
            "LUCKY777": {"coins": 777, "description": "Lucky bonus"},
            "GACHA1000": {"coins": 1000, "description": "Premium bonus"},
            "FREEGEMS": {"coins": 250, "description": "Free gems"}
        }
        self.available_codes = default_codes
        self._save_codes()
    
    def _load_codes(self):
        """Load available codes from file"""
        try:
            if os.path.exists(self.codes_file):
                with open(self.codes_file, 'r') as f:
                    self.available_codes = json.load(f)
        except Exception as e:
            print(f"Error loading codes: {e}")
            self.available_codes = {}
    
    def _save_codes(self):
        """Save available codes to file"""
        try:
            Path(self.codes_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.codes_file, 'w') as f:
                json.dump(self.available_codes, f, indent=2)
        except Exception as e:
            print(f"Error saving codes: {e}")
    
    def _load_used_codes(self):
        """Load used codes from file"""
        try:
            if os.path.exists(self.used_codes_file):
                with open(self.used_codes_file, 'r') as f:
                    data = json.load(f)
                    self.used_codes = set(data.get('codes', []))
        except Exception as e:
            print(f"Error loading used codes: {e}")
            self.used_codes = set()
    
    def _save_used_codes(self):
        """Save used codes to file"""
        try:
            Path(self.used_codes_file).parent.mkdir(parents=True, exist_ok=True)
            with open(self.used_codes_file, 'w') as f:
                json.dump({'codes': list(self.used_codes)}, f, indent=2)
        except Exception as e:
            print(f"Error saving used codes: {e}")
    
    def redeem_code(self, code: str) -> tuple[bool, str, int]:
        """
        Attempt to redeem a code
        
        Args:
            code: The code to redeem (case-insensitive)
            
        Returns:
            tuple: (success, message, coins_awarded)
        """
        # Normalize code to uppercase
        code = code.strip().upper()
        
        # Check if code is empty
        if not code:
            return False, "Please enter a code", 0
        
        # Check if code exists
        if code not in self.available_codes:
            return False, "Invalid code", 0
        
        # Check if code has been used
        if code in self.used_codes:
            return False, "Code already used", 0
        
        # Redeem the code
        code_data = self.available_codes[code]
        coins = code_data.get('coins', 0)
        description = code_data.get('description', 'Bonus')
        
        # Mark code as used
        self.used_codes.add(code)
        self._save_used_codes()
        
        return True, f"{description}: +{coins} coins!", coins
    
    def add_code(self, code: str, coins: int, description: str = "Bonus") -> bool:
        """
        Add a new redeem code (admin function)
        
        Args:
            code: The code string
            coins: Number of coins to award
            description: Description of the code
            
        Returns:
            bool: True if code was added, False if it already exists
        """
        code = code.strip().upper()
        
        if code in self.available_codes:
            return False
        
        self.available_codes[code] = {
            'coins': coins,
            'description': description
        }
        self._save_codes()
        return True
    
    def remove_code(self, code: str) -> bool:
        """
        Remove a redeem code (admin function)
        
        Args:
            code: The code to remove
            
        Returns:
            bool: True if code was removed, False if it didn't exist
        """
        code = code.strip().upper()
        
        if code in self.available_codes:
            del self.available_codes[code]
            self._save_codes()
            return True
        return False
    
    def get_all_codes(self) -> dict:
        """
        Get all available codes (admin function)
        
        Returns:
            dict: All available codes and their data
        """
        return self.available_codes.copy()
    
    def is_code_used(self, code: str) -> bool:
        """
        Check if a code has been used
        
        Args:
            code: The code to check
            
        Returns:
            bool: True if code has been used
        """
        return code.strip().upper() in self.used_codes
