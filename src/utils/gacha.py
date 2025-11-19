"""
ฟังก์ชันสำหรับระบบสุ่มตัวละคร (Gacha)
ไม่ใช้ OOP - เขียนแบบฟังก์ชันธรรมดา
"""

import random
from src.data.hero_data import get_heroes_by_rarity
from src.core.config import RARITY_RATES


def calculate_rarity(rates=None):
    """
    สุ่ม rarity ตามอัตราที่กำหนด
    
    Args:
        rates: dict ของอัตรา (ถ้าไม่ระบุจะใช้ค่าเริ่มต้น)
    
    Returns:
        str: rarity ('rare', 'epic', 'legendary', 'extreme')
    """
    if rates is None:
        rates = RARITY_RATES
    
    roll = random.random()
    cumulative = 0.0
    
    # เรียงจากหายากที่สุดไปหายากน้อยสุด
    for rarity in ['extreme', 'legendary', 'epic', 'rare']:
        if rarity in rates:
            cumulative += rates[rarity]
            if roll <= cumulative:
                return rarity
    
    return 'rare'  # fallback


def random_hero(rarity=None, rates=None):
    """
    สุ่มตัวละคร
    
    Args:
        rarity: rarity ที่ต้องการ (ถ้าไม่ระบุจะสุ่ม)
        rates: อัตราการสุ่ม (ถ้าไม่ระบุจะใช้ค่าเริ่มต้น)
    
    Returns:
        Character: ตัวละครที่สุ่มได้
    """
    # ถ้าไม่ระบุ rarity ให้สุ่ม
    if rarity is None:
        rarity = calculate_rarity(rates)
    
    # หาตัวละครที่มี rarity นี้
    heroes = get_heroes_by_rarity(rarity)
    
    if not heroes:
        # ถ้าไม่มี ให้ใช้ rare แทน
        heroes = get_heroes_by_rarity('rare')
    
    # สุ่มตัวละคร
    return random.choice(heroes)


def summon(count=1, rates=None):
    """
    สุ่มตัวละครหลายตัว
    
    Args:
        count: จำนวนที่ต้องการสุ่ม
        rates: อัตราการสุ่ม
    
    Returns:
        list: list ของตัวละครที่สุ่มได้
    """
    heroes = []
    for _ in range(count):
        hero = random_hero(rates=rates)
        heroes.append(hero)
    return heroes


def summon_mystic(count=1):
    """
    สุ่ม Mystic Chest (ไม่มี extreme)
    
    Args:
        count: จำนวนที่ต้องการสุ่ม
    
    Returns:
        list: list ของตัวละครที่สุ่มได้
    """
    mystic_rates = {
        'rare': 0.70,
        'epic': 0.25,
        'legendary': 0.05
    }
    return summon(count, mystic_rates)


def summon_celestial(count=1):
    """
    สุ่ม Celestial Chest (มี extreme)
    
    Args:
        count: จำนวนที่ต้องการสุ่ม
    
    Returns:
        list: list ของตัวละครที่สุ่มได้
    """
    return summon(count, RARITY_RATES)

