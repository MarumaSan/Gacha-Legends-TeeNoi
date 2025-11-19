"""
ฟังก์ชันสำหรับจัดการโค้ดแลกรางวัล
ไม่ใช้ OOP - เขียนแบบฟังก์ชันธรรมดา
"""

import json
import os
from pathlib import Path


# # โค้ดเริ่มต้น
# DEFAULT_CODES = {
#     "WELCOME2024": {"coins": 500, "description": "Welcome bonus"},
#     "HERO100": {"coins": 100, "description": "Starter pack"},
#     "LUCKY777": {"coins": 777, "description": "Lucky bonus"},
#     "GACHA1000": {"coins": 1000, "description": "Premium bonus"},
#     "FREEGEMS": {"coins": 250, "description": "Free gems"}
# }


def load_available_codes():
    """
    โหลดโค้ดที่มีทั้งหมด
    
    Returns:
        dict: โค้ดทั้งหมด
    """
    filepath = "data/json/codes.json"
    
    if not os.path.exists(filepath):
        # สร้างไฟล์ใหม่ด้วยโค้ดเริ่มต้น
        save_available_codes(DEFAULT_CODES)
        return DEFAULT_CODES.copy()
    
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading codes: {e}")
        return DEFAULT_CODES.copy()


def save_available_codes(codes):
    """บันทึกโค้ดทั้งหมด"""
    filepath = "data/json/codes.json"
    
    try:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(codes, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving codes: {e}")
        return False


def load_used_codes(player_slot):
    """
    โหลดโค้ดที่ใช้แล้วของผู้เล่น
    
    Args:
        player_slot: slot ของผู้เล่น (1 หรือ 2)
    
    Returns:
        set: โค้ดที่ใช้แล้ว
    """
    filepath = f"data/json/used_codes_player{player_slot}.json"
    
    if not os.path.exists(filepath):
        return set()
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return set(data.get('codes', []))
    except Exception as e:
        print(f"Error loading used codes: {e}")
        return set()


def save_used_codes(used_codes, player_slot):
    """บันทึกโค้ดที่ใช้แล้ว"""
    filepath = f"data/json/used_codes_player{player_slot}.json"
    
    try:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump({'codes': list(used_codes)}, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving used codes: {e}")
        return False


def redeem_code(code, player_slot):
    """
    ใช้โค้ดแลกรางวัล
    
    Args:
        code: โค้ดที่ต้องการใช้
        player_slot: slot ของผู้เล่น
    
    Returns:
        tuple: (success, message, coins)
    """
    code = code.strip().upper()
    
    if not code:
        return False, "Please enter a code", 0
    
    # โหลดโค้ดที่มี
    available_codes = load_available_codes()
    
    if code not in available_codes:
        return False, "Invalid code", 0
    
    # โหลดโค้ดที่ใช้แล้ว
    used_codes = load_used_codes(player_slot)
    
    if code in used_codes:
        return False, "Code already used", 0
    
    # ใช้โค้ด
    code_data = available_codes[code]
    coins = code_data.get('coins', 0)
    description = code_data.get('description', 'Bonus')
    
    # บันทึกว่าใช้แล้ว
    used_codes.add(code)
    save_used_codes(used_codes, player_slot)
    
    return True, f"{description}: +{coins} coins!", coins


def add_code(code, coins, description="Bonus"):
    """เพิ่มโค้ดใหม่ (สำหรับ admin)"""
    code = code.strip().upper()
    
    available_codes = load_available_codes()
    
    if code in available_codes:
        return False
    
    available_codes[code] = {
        'coins': coins,
        'description': description
    }
    
    save_available_codes(available_codes)
    return True

