"""
ฟังก์ชันสำหรับจัดการข้อมูลผู้เล่น
"""

import json
import os
from pathlib import Path
from src.core.config import STARTING_COINS


def create_player_data():
    """
    สร้างข้อมูลผู้เล่นใหม่
    
    Returns:
        dict: ข้อมูลผู้เล่น
    """
    return {
        'coins': STARTING_COINS,
        'owned_heroes': [],
        'settings': {
            'volume': 10,
            'sound_enabled': True
        },
        'rank': 0
    }


def save_player_data(player_data, player_slot):
    """
    บันทึกข้อมูลผู้เล่น
    
    Args:
        player_data: dict ข้อมูลผู้เล่น
        player_slot: slot ของผู้เล่น (1 หรือ 2)
    
    Returns:
        bool: สำเร็จหรือไม่
    """
    filepath = f"data/json/save_data_player{player_slot}.json"
    
    try:
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(player_data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving player data: {e}")
        return False


def load_player_data(player_slot):
    """
    โหลดข้อมูลผู้เล่น
    
    Args:
        player_slot: slot ของผู้เล่น (1 หรือ 2)
    
    Returns:
        dict: ข้อมูลผู้เล่น (ถ้าไม่มีจะสร้างใหม่)
    """
    filepath = f"data/json/save_data_player{player_slot}.json"
    
    if not os.path.exists(filepath):
        print(f"No save file found for Player {player_slot} - creating new")
        return create_player_data()
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # ตรวจสอบว่ามีข้อมูลครบ
        if 'coins' not in data:
            data['coins'] = STARTING_COINS
        if 'owned_heroes' not in data:
            data['owned_heroes'] = []
        if 'settings' not in data:
            data['settings'] = {'volume': 50, 'sound_enabled': True}
        if 'rank' not in data:
            data['rank'] = 0
        
        return data
    except Exception as e:
        print(f"Error loading player data: {e}")
        return create_player_data()


def add_coins(player_data, amount):
    """เพิ่มเหรียญ"""
    if amount > 0:
        player_data['coins'] += amount


def spend_coins(player_data, amount):
    """
    ใช้เหรียญ
    
    Returns:
        bool: สำเร็จหรือไม่ (มีเหรียญพอหรือไม่)
    """
    if amount <= 0:
        return False
    
    if player_data['coins'] >= amount:
        player_data['coins'] -= amount
        return True
    return False


def add_hero(player_data, hero_id):
    """
    เพิ่มตัวละคร
    
    Returns:
        bool: เป็นตัวใหม่หรือไม่
    """
    if hero_id not in player_data['owned_heroes']:
        player_data['owned_heroes'].append(hero_id)
        return True
    return False


def has_hero(player_data, hero_id):
    """ตรวจสอบว่ามีตัวละครหรือไม่"""
    return hero_id in player_data['owned_heroes']


def get_total_power(player_data):
    """คำนวณพลังรวม"""
    from src.data.hero_data import get_hero
    
    total = 0
    for hero_id in player_data['owned_heroes']:
        hero = get_hero(hero_id)
        if hero:
            total += hero.power
    return total

