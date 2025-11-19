"""Profile state - display player statistics and owned heroes"""

import pygame
from src.core.game_state import GameState
from src.ui.button import Button
from src.ui.text_display import TextDisplay
from src.utils import assets

from src.data.hero_data import get_hero, get_all_heroes
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GOLD, COLOR_WHITE
from src.ui.image_button import _ImageButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game


class ProfileState(GameState):
    """Profile screen showing player stats and owned heroes"""
    
    def __init__(self, game: 'Game', player_data):
        """
        Initialize the profile state
        
        Args:
            game: Reference to the main Game instance
            player_data instance for accessing player information
        """
        super().__init__(game)
        self.player_data = player_data
        self.background = None
        self.font_title = None
        self.font_large = None
        self.font_normal = None
        self.font_small = None
        
        # UI elements
        self.back_button = None
        self.leaderboard_button = None
        self.leaderboard_data = []
    
    def enter(self):
        """Called when entering this state - load assets and create UI"""
        # Load background (book-style interface)
        try:
            self.background = assets.load_image('assets/backgrounds/book.png', 
                                                     (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Warning: Could not load background: {e}")
            # Create a fallback background
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((40, 30, 20))
        
        # Load fonts (ใช้ฟอนต์เล็กลง)
        try:
            self.font_title = assets.load_font('assets/fonts/Monocraft.ttf', 25)
            self.font_large = assets.load_font('assets/fonts/Monocraft.ttf', 18)
            self.font_normal = assets.load_font('assets/fonts/Monocraft.ttf', 14)
            self.font_small = assets.load_font('assets/fonts/Monocraft.ttf', 12)
        except Exception as e:
            print(f"Warning: Could not load font: {e}")
            self.font_title = pygame.font.Font(None, 25)
            self.font_large = pygame.font.Font(None, 18)
            self.font_normal = pygame.font.Font(None, 16)
            self.font_small = pygame.font.Font(None, 14)
        
        # โหลดรูปปุ่ม (ใช้รูปเดียวกับหน้าแรก)
        try:
            button_img = assets.load_image('assets/ui/12.png').convert_alpha()
        except Exception as e:
            print(f"Warning: Could not load button image: {e}")
            button_img = pygame.Surface((220, 70), pygame.SRCALPHA)
            button_img.fill((60, 60, 90, 255))
            pygame.draw.rect(button_img, (255, 255, 255, 40), button_img.get_rect(), border_radius=16)
        
        # ปุ่ม RETURN TO LOBBY (วางไว้ล่างสุด ขยายขนาดให้ใหญ่ขึ้น)
        button_center_y = SCREEN_HEIGHT - 60
        self.back_button = _ImageButton(
            button_img,
            center=(SCREEN_WIDTH // 2, button_center_y),
            on_click=self.on_back_click,
            scale=1.5,  
            use_mask=True,
            text="RETURN TO LOBBY",
            font=self.font_small
        )
        
        # ปุ่ม VIEW FULL LEADERBOARD (วางไว้ใต้ตาราง leaderboard)
        self.leaderboard_button = _ImageButton(
            button_img,
            center=(SCREEN_WIDTH * 3 // 4 - 130, SCREEN_HEIGHT - 200),
            on_click=self.on_leaderboard_click,
            scale=1.0,
            use_mask=True,
            text="VIEW FULL",
            font=self.font_small
        )
        
        # โหลดข้อมูล leaderboard
        self._load_leaderboard_data()
    
    def _load_leaderboard_data(self):
        """โหลดข้อมูล Player 1 และ Player 2 แล้วเรียงตามแต้มชนะ"""
        from src.utils import player
        
        self.leaderboard_data = []
        
        for slot in [1, 2]:
            data = player.load_player_data(slot)
            rank = data.get('rank', 0)  # แต้มชนะ
            
            self.leaderboard_data.append({
                'slot': slot,
                'name': f'Player {slot}',
                'rank': rank
            })
        
        # เรียงตามแต้มชนะ (มากไปน้อย)
        self.leaderboard_data.sort(key=lambda x: x['rank'], reverse=True)
    
    def on_back_click(self):
        """Callback for Return button - go back to main lobby"""
        self.game.change_state('main_lobby')
    
    def on_leaderboard_click(self):
        """Callback for Leaderboard button - go to full leaderboard"""
        self.game.change_state('leaderboard')
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: pygame.event.Event object
        """
        # Handle back button
        if self.back_button:
            self.back_button.handle_event(event)
        if self.leaderboard_button:
            self.leaderboard_button.handle_event(event)
    
    def update(self, dt):
        """
        Update game state logic
        
        Args:
            dt: Delta time in seconds since last update
        """
        # Update back button
        if self.back_button:
            self.back_button.update(dt)
        if self.leaderboard_button:
            self.leaderboard_button.update(dt)
    
    def draw(self, screen):
        """
        Draw the profile state to the screen
        
        Args:
            screen: pygame.Surface to draw on
        """
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
        
        # คำนวณข้อมูลผู้เล่น
        total_power = sum(get_hero(hero_id).power for hero_id in self.player_data['owned_heroes'] if get_hero(hero_id))
        collected = len(self.player_data['owned_heroes'])
        total_heroes = 21  # จำนวนฮีโร่ทั้งหมด
        all_gold = self.player_data['coins']
        
        # ===== หน้าซ้าย - STATISTICS (สถิติผู้เล่น) =====
        left_x = SCREEN_WIDTH // 4 + 130  # ตำแหน่ง X ของหน้าซ้าย (ขยับขวา 130px)
        left_start_y = 120  # ตำแหน่ง Y เริ่มต้น (ขยับขึ้น)
        
        # หัวข้อ STATISTICS
        if self.font_title:
            stats_title = self.font_title.render("STATISTICS", True, (0, 0, 0))
            screen.blit(stats_title, (left_x - stats_title.get_width() // 2, left_start_y))
        
        # แสดง TOTAL POWER (พลังรวมของฮีโร่ทั้งหมด)
        if self.font_normal:
            power_label = self.font_normal.render("TOTAL POWER", True, (0, 0, 0))
            screen.blit(power_label, (left_x - power_label.get_width() // 2, left_start_y + 90))
            
            power_value = self.font_large.render(str(total_power), True, (0, 0, 0))
            screen.blit(power_value, (left_x - power_value.get_width() // 2, left_start_y + 120))
        
        # แสดง COLLECTED (จำนวนฮีโร่ที่สะสมได้ / ทั้งหมด)
        if self.font_normal:
            collected_label = self.font_normal.render("COLLECTED", True, (0, 0, 0))
            screen.blit(collected_label, (left_x - collected_label.get_width() // 2, left_start_y + 210))
            
            collected_value = self.font_large.render(f"{collected} / {total_heroes}", True, (0, 0, 0))
            screen.blit(collected_value, (left_x - collected_value.get_width() // 2, left_start_y + 240))
        
        # แสดง ALL GOLD (จำนวนเหรียญทั้งหมด)
        if self.font_normal:
            gold_label = self.font_normal.render("ALL GOLD", True, (0, 0, 0))
            screen.blit(gold_label, (left_x - gold_label.get_width() // 2, left_start_y + 330))
            
            gold_value = self.font_large.render(str(all_gold), True, (0, 0, 0))
            screen.blit(gold_value, (left_x - gold_value.get_width() // 2, left_start_y + 360))
        
        # ===== หน้าขวา - LEADERBOARD (กระดานผู้นำ) =====
        right_x = SCREEN_WIDTH * 3 // 4 - 130  # ตำแหน่ง X ของหน้าขวา (ขยับซ้าย 130px)
        right_start_y = 120  # ตำแหน่ง Y เริ่มต้น (ขยับขึ้น)
        
        # หัวข้อ LEADERBOARD
        if self.font_title:
            leader_title = self.font_title.render("LEADERBOARD", True, (0, 0, 0))
            screen.blit(leader_title, (right_x - leader_title.get_width() // 2, right_start_y))
        
        # หัวตาราง NAME และ WINS
        if self.font_normal:
            name_header = self.font_normal.render("NAME", True, (0, 0, 0))
            wins_header = self.font_normal.render("WINS", True, (0, 0, 0))
            
            screen.blit(name_header, (right_x - 100, right_start_y + 90))
            screen.blit(wins_header, (right_x + 50, right_start_y + 90))
        
        # แสดงรายชื่อและแต้มชนะในกระดานผู้นำ (Player 1 และ Player 2)
        if self.font_normal:
            for i, entry in enumerate(self.leaderboard_data[:5]):  # แสดงสูงสุด 5 อันดับ
                y_pos = right_start_y + 130 + (i * 40)
                
                # แสดงอันดับ
                rank_num_text = self.font_normal.render(f"#{i+1}", True, (0, 0, 0))
                screen.blit(rank_num_text, (right_x - 130, y_pos))
                
                # แสดงชื่อ (ถ้าเป็น player ปัจจุบันให้แสดง "ME")
                current_slot = self.game.current_player_slot if hasattr(self.game, 'current_player_slot') else None
                display_name = "ME" if entry['slot'] == current_slot else entry['name']
                name_text = self.font_normal.render(display_name, True, (0, 0, 0))
                screen.blit(name_text, (right_x - 90, y_pos))
                
                # แสดงแต้มชนะ
                wins_text = self.font_normal.render(str(entry['rank']), True, (0, 0, 0))
                screen.blit(wins_text, (right_x + 65, y_pos))
        
        # ปุ่ม VIEW FULL LEADERBOARD
        if self.leaderboard_button:
            self.leaderboard_button.draw(screen)
        
        # ปุ่ม RETURN TO LOBBY (กลับไปหน้าล็อบบี้)
        if self.back_button:
            self.back_button.draw(screen)
    
    def exit(self):
        """Called when exiting this state"""
        pass
