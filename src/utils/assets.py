"""
ฟังก์ชันสำหรับโหลดและจัดการ assets (รูป, เสียง, ฟอนต์)
ไม่ใช้ OOP - เขียนแบบฟังก์ชันธรรมดา
"""

import pygame
import os

# Cache สำหรับเก็บ assets ที่โหลดแล้ว
_image_cache = {}
_font_cache = {}
_sound_cache = {}


def load_image(path, scale=None):
    """
    โหลดรูปภาพ
    
    Args:
        path: path ของรูป
        scale: (width, height) ถ้าต้องการปรับขนาด
    
    Returns:
        pygame.Surface
    """
    # สร้าง cache key
    cache_key = f"{path}_{scale}" if scale else path
    
    # ถ้ามีใน cache แล้ว ใช้เลย
    if cache_key in _image_cache:
        return _image_cache[cache_key]
    
    # ตรวจสอบว่าไฟล์มีจริง
    if not os.path.exists(path):
        print(f"Warning: Image not found: {path}")
        # สร้างรูปสำรอง
        surface = pygame.Surface((100, 100))
        surface.fill((200, 200, 200))
        return surface
    
    try:
        # โหลดรูป
        image = pygame.image.load(path)
        
        # ปรับขนาดถ้าต้องการ
        if scale:
            image = pygame.transform.scale(image, scale)
        
        # Convert เพื่อ performance
        try:
            image = image.convert_alpha()
        except:
            pass
        
        # เก็บใน cache
        _image_cache[cache_key] = image
        
        return image
    except Exception as e:
        print(f"Error loading image {path}: {e}")
        # สร้างรูปสำรอง
        surface = pygame.Surface((100, 100))
        surface.fill((200, 200, 200))
        return surface


def load_font(path, size):
    """
    โหลดฟอนต์
    
    Args:
        path: path ของฟอนต์
        size: ขนาดฟอนต์
    
    Returns:
        pygame.font.Font
    """
    cache_key = f"{path}_{size}"
    
    if cache_key in _font_cache:
        return _font_cache[cache_key]
    
    if not os.path.exists(path):
        print(f"Warning: Font not found: {path}")
        return pygame.font.Font(None, size)
    
    try:
        font = pygame.font.Font(path, size)
        _font_cache[cache_key] = font
        return font
    except Exception as e:
        print(f"Error loading font {path}: {e}")
        return pygame.font.Font(None, size)


def load_sound(path):
    """
    โหลดเสียง
    
    Args:
        path: path ของเสียง
    
    Returns:
        pygame.mixer.Sound
    """
    if path in _sound_cache:
        return _sound_cache[path]
    
    if not os.path.exists(path):
        print(f"Warning: Sound not found: {path}")
        return None
    
    try:
        sound = pygame.mixer.Sound(path)
        _sound_cache[path] = sound
        return sound
    except Exception as e:
        print(f"Error loading sound {path}: {e}")
        return None


def clear_cache():
    """ล้าง cache ทั้งหมด"""
    _image_cache.clear()
    _font_cache.clear()
    _sound_cache.clear()

