"""How to Play state - หน้าแสดงวิธีเล่น"""

import pygame
from src.core.game_state import GameState
from src.utils import assets
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui.image_button import _ImageButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game


class HowToPlayState(GameState):
    """หน้าแสดงวิธีเล่น - มีรูป 17 หน้า"""
    
    def __init__(self, game: 'Game'):
        super().__init__(game)
        
        self.current_page = 1  # หน้าแรก
        self.total_pages = 17  # จำนวนหน้าทั้งหมด
        
        self.background = None
        self.font_small = None
        
        # ปุ่ม
        self.left_button = None
        self.right_button = None
        
        # รูปภาพทั้งหมด
        self.page_images = {}
    
    def enter(self):
        """เรียกเมื่อเข้าสู่หน้านี้"""
        # โหลดฟอนต์
        try:
            self.font_small = assets.load_font('assets/fonts/Monocraft.ttf', 15)
        except Exception as e:
            print(f"Warning: Could not load font: {e}")
            self.font_small = pygame.font.Font(None, 15)
        
        # โหลดรูปภาพทั้งหมด
        for i in range(1, self.total_pages + 1):
            try:
                img = assets.load_image(f'assets/How_to_play/{i}.png', (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.page_images[i] = img
            except Exception as e:
                print(f"Warning: Could not load page {i}: {e}")
                # สร้างรูปสำรอง
                fallback = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                fallback.fill((40, 30, 20))
                self.page_images[i] = fallback
        
        # โหลดรูปปุ่ม
        try:
            left_img = assets.load_image('assets/ui/left botton.png')
            right_img = assets.load_image('assets/ui/right botton.png')
        except Exception as e:
            print(f"Warning: Could not load button images: {e}")
            left_img = pygame.Surface((60, 60), pygame.SRCALPHA)
            right_img = pygame.Surface((60, 60), pygame.SRCALPHA)
            left_img.fill((100, 80, 60, 200))
            right_img.fill((100, 80, 60, 200))
        
        # ปุ่มซ้าย (หน้าก่อนหน้า)
        self.left_button = _ImageButton(
            left_img,
            center=(100, SCREEN_HEIGHT // 2),
            on_click=self.on_prev_page,
            scale=1.0,
            use_mask=True
        )
        
        # ปุ่มขวา (หน้าถัดไป)
        self.right_button = _ImageButton(
            right_img,
            center=(SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2),
            on_click=self.on_next_page,
            scale=1.0,
            use_mask=True
        )
        
        # รีเซ็ตหน้า
        self.current_page = 1
    
    def on_prev_page(self):
        """ไปหน้าก่อนหน้า"""
        if self.current_page > 1:
            self.current_page -= 1
    
    def on_next_page(self):
        """ไปหน้าถัดไป หรือกลับไปหน้า loading ถ้าถึงหน้าสุดท้าย"""
        if self.current_page < self.total_pages:
            self.current_page += 1
        else:
            # ถึงหน้าสุดท้ายแล้ว กลับไปหน้า loading
            self.game.change_state('loading')
    
    def handle_event(self, event):
        """จัดการ event"""
        if self.left_button:
            self.left_button.handle_event(event)
        if self.right_button:
            self.right_button.handle_event(event)
    
    def update(self, dt):
        """อัปเดตสถานะ"""
        if self.left_button:
            self.left_button.update(dt)
        if self.right_button:
            self.right_button.update(dt)
    
    def draw(self, screen):
        """วาดหน้าจอ"""
        # วาดรูปภาพหน้าปัจจุบัน
        if self.current_page in self.page_images:
            screen.blit(self.page_images[self.current_page], (0, 0))
        
        # วาดปุ่ม
        if self.left_button:
            self.left_button.draw(screen)
        if self.right_button:
            self.right_button.draw(screen)
        
        # แสดงหมายเลขหน้าด้านบน
        if self.font_small:
            page_text = f"{self.current_page} / {self.total_pages}"
            page_surf = self.font_small.render(page_text, True, (255, 255, 255))
            screen.blit(page_surf, (SCREEN_WIDTH // 2 - page_surf.get_width() // 2, 20))
    
    def exit(self):
        """เรียกเมื่อออกจากหน้านี้"""
        pass
