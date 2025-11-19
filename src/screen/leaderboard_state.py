"""Leaderboard state - แสดงอันดับ Player 1 และ Player 2"""

import pygame
from src.core.game_state import GameState
from src.utils import assets, player
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui.image_button import _ImageButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game


class LeaderboardState(GameState):
    """หน้าแสดงอันดับ Player 1 และ Player 2"""
    
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.background = None
        self.font_title = None
        self.font_large = None
        self.font_normal = None
        self.font_small = None
        self.back_button = None
        self.leaderboard_data = []
    
    def enter(self):
        """เรียกเมื่อเข้าสู่หน้านี้"""
        # โหลดพื้นหลัง
        try:
            self.background = assets.load_image('assets/backgrounds/town_2.png', 
                                                     (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Warning: Could not load background: {e}")
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((40, 30, 50))
        
        # โหลดฟอนต์
        try:
            self.font_title = assets.load_font('assets/fonts/Monocraft.ttf', 48)
            self.font_large = assets.load_font('assets/fonts/Monocraft.ttf', 32)
            self.font_normal = assets.load_font('assets/fonts/Monocraft.ttf', 24)
            self.font_small = assets.load_font('assets/fonts/Monocraft.ttf', 15)
        except Exception as e:
            print(f"Warning: Could not load font: {e}")
            self.font_title = pygame.font.Font(None, 48)
            self.font_large = pygame.font.Font(None, 32)
            self.font_normal = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 15)
        
        # โหลดข้อมูล Player 1 และ Player 2
        self._load_leaderboard_data()
        
        # โหลดรูปปุ่ม
        try:
            button_img = assets.load_image('assets/ui/12.png').convert_alpha()
        except Exception as e:
            print(f"Warning: Could not load button image: {e}")
            button_img = pygame.Surface((220, 70), pygame.SRCALPHA)
            button_img.fill((60, 60, 90, 255))
            pygame.draw.rect(button_img, (255, 255, 255, 40), button_img.get_rect(), border_radius=16)
        
        # ปุ่ม BACK
        back_y = SCREEN_HEIGHT - 60
        self.back_button = _ImageButton(
            button_img,
            center=(SCREEN_WIDTH // 2, back_y),
            on_click=self.on_back_click,
            scale=1.2,
            use_mask=True,
            text="BACK",
            font=self.font_small
        )
    
    def _load_leaderboard_data(self):
        """โหลดข้อมูล Player 1 และ Player 2 แล้วเรียงตามแต้มชนะ"""
        self.leaderboard_data = []
        
        for slot in [1, 2]:
            data = player.load_player_data(slot)
            rank = data.get('rank', 0)  # แต้มชนะ
            hero_count = len(data['owned_heroes'])
            coins = data['coins']
            
            self.leaderboard_data.append({
                'slot': slot,
                'name': f'Player {slot}',
                'rank': rank,
                'heroes': hero_count,
                'coins': coins
            })
        
        # เรียงตามแต้มชนะ (มากไปน้อย)
        self.leaderboard_data.sort(key=lambda x: x['rank'], reverse=True)
    
    def on_back_click(self):
        """กลับไปหน้าล็อบบี้"""
        self.game.change_state('main_lobby')
    
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
        
        # วาดหัวข้อ LEADERBOARD
        if self.font_title:
            title = self.font_title.render("LEADERBOARD", True, (255, 215, 0))
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 80))
        
        # วาดตาราง
        start_y = 200
        row_height = 100
        
        for i, entry in enumerate(self.leaderboard_data):
            y = start_y + i * row_height
            
            # กรอบพื้นหลัง
            rank_color = (255, 215, 0) if i == 0 else (192, 192, 192) if i == 1 else (205, 127, 50)
            bg_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, y, 600, 80)
            pygame.draw.rect(screen, (0, 0, 0, 150), bg_rect, border_radius=10)
            pygame.draw.rect(screen, rank_color, bg_rect, 3, border_radius=10)
            
            # อันดับ
            rank_text = f"#{i + 1}"
            if self.font_large:
                rank_surf = self.font_large.render(rank_text, True, rank_color)
                screen.blit(rank_surf, (bg_rect.x + 20, bg_rect.y + 25))
            
            # ชื่อผู้เล่น
            if self.font_normal:
                name_surf = self.font_normal.render(entry['name'], True, (255, 255, 255))
                screen.blit(name_surf, (bg_rect.x + 120, bg_rect.y + 15))
            
            # ข้อมูล
            if self.font_small:
                info_text = f"Wins: {entry['rank']}  |  Heroes: {entry['heroes']}  |  Coins: {entry['coins']}"
                info_surf = self.font_small.render(info_text, True, (200, 200, 200))
                screen.blit(info_surf, (bg_rect.x + 120, bg_rect.y + 45))
        
        # วาดปุ่ม BACK
        if self.back_button:
            self.back_button.draw(screen)
    
    def exit(self):
        """เรียกเมื่อออกจากหน้านี้"""
        pass
