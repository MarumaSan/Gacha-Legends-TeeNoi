"""Celestial Info state - แสดงตัวละครและ rate ที่สุ่มได้จาก Celestial Chest"""

import pygame
from src.core.game_state import GameState
from src.utils import assets
from src.data.hero_data import get_heroes_by_rarity
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui.image_button import _ImageButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

class CelestialInfoState(GameState):
    """หน้าแสดงข้อมูล Celestial Chest - ตัวละครและ rate"""
    
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.background = None
        self.font_title = None
        self.font_normal = None
        self.font_small = None
        self.back_button = None
        
        # ข้อมูลตัวละครแยกตาม rarity
        self.heroes_by_rarity = {}
        
        # Celestial Chest rates (มี EXTREME)
        self.rates = {
            'extreme': 0.01, 
            'legendary': 0.04, 
            'epic': 0.25,      
            'rare': 0.70        
        }
        
        # สีของแต่ละ rarity
        self.rarity_colors = {
            'extreme': (255,82,82),        # แดง
            'legendary': (255, 215, 0),    # ทอง
            'epic': (147, 112, 219),       # ม่วง
            'rare': (100, 149, 237)        # น้ำเงิน
        }
    
    def enter(self):
        """เรียกเมื่อเข้าสู่หน้านี้"""
        # โหลดพื้นหลัง
        try:
            self.background = assets.load_image('assets/backgrounds/summon_2.png', 
                                                     (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Warning: Could not load background: {e}")
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((40, 30, 20))
        
        # โหลดฟอนต์
        try:
            self.font_title = assets.load_font('assets/fonts/Monocraft.ttf', 28)
            self.font_normal = assets.load_font('assets/fonts/Monocraft.ttf', 18)
            self.font_small = assets.load_font('assets/fonts/Monocraft.ttf', 15)
        except Exception as e:
            print(f"Warning: Could not load font: {e}")
            self.font_title = pygame.font.Font(None, 28)
            self.font_normal = pygame.font.Font(None, 18)
            self.font_small = pygame.font.Font(None, 15)
        
        # โหลดข้อมูลตัวละคร
        self.heroes_by_rarity = {
            'extreme': get_heroes_by_rarity('extreme'),
            'legendary': get_heroes_by_rarity('legendary'),
            'epic': get_heroes_by_rarity('epic'),
            'rare': get_heroes_by_rarity('rare')
        }
        
        # โหลดรูปปุ่ม
        try:
            button_img = assets.load_image('assets/ui/12.png').convert_alpha()
        except Exception as e:
            print(f"Warning: Could not load button image: {e}")
            button_img = pygame.Surface((220, 70), pygame.SRCALPHA)
            button_img.fill((60, 60, 90, 255))
        
        # ปุ่ม BACK
        self.back_button = _ImageButton(
            button_img,
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60),
            on_click=self.on_back_click,
            scale=1.2,
            use_mask=True,
            text="BACK",
            font=self.font_small
        )
    
    def on_back_click(self):
        """กลับไปหน้าสุ่ม"""
        self.game.change_state('celestial_chest')
    
    def handle_event(self, event):
        """จัดการ event"""
        if self.back_button:
            self.back_button.handle_event(event)
    
    def update(self, dt):
        """อัปเดตสถานะ"""
        if self.back_button:
            self.back_button.update(dt)
    
    def draw(self, screen):
        """วาดหน้าจอ"""
        # วาดพื้นหลัง
        if self.background:
            screen.blit(self.background, (0, 0))
        
        # หัวข้อ
        if self.font_title:
            title = self.font_title.render("CELESTIAL CHEST - DROP RATES", True, (255, 255, 255))
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 40))
        
        # แสดง rate แต่ละ rarity
        start_y = 100
        
        card_width = 60
        card_height = 84
        card_spacing = 10
        max_cards_per_row = 10
        
        for rarity in ['extreme', 'legendary', 'epic', 'rare']:
            heroes = self.heroes_by_rarity.get(rarity, [])
            rate = self.rates[rarity]
            color = self.rarity_colors[rarity]
            
            # หัวข้อ rarity และ rate
            if self.font_normal:
                rarity_text = f"{rarity.upper()} - {rate*100:.0f}%"
                rarity_surf = self.font_normal.render(rarity_text, True, color)
                screen.blit(rarity_surf, (SCREEN_WIDTH // 2 - rarity_surf.get_width() // 2, start_y))
            
            # แสดงการ์ดตัวละคร
            card_y = start_y + 30
            display_heroes = heroes[:max_cards_per_row]
            cards_in_row = len(display_heroes)
            if cards_in_row:
                row_width = cards_in_row * card_width + (cards_in_row - 1) * card_spacing
                card_x = SCREEN_WIDTH // 2 - row_width // 2
            else:
                card_x = SCREEN_WIDTH // 2
            
            for i, hero in enumerate(display_heroes):
                try:
                    card_img = assets.load_image(hero.card_front_path, (card_width, card_height))
                    screen.blit(card_img, (card_x + i * (card_width + card_spacing), card_y))
                except Exception as e:
                    # สร้างการ์ดสำรอง
                    fallback = pygame.Surface((card_width, card_height))
                    fallback.fill(color)
                    screen.blit(fallback, (card_x + i * (card_width + card_spacing), card_y))
            
            start_y += 130
        
        # ปุ่ม BACK
        if self.back_button:
            self.back_button.draw(screen)
    
    def exit(self):
        """เรียกเมื่อออกจากหน้านี้"""
        pass
