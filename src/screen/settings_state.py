"""Settings state - game settings and code redemption"""

import pygame
from src.core.game_state import GameState
from src.ui.button import Button
from src.ui.slider import Slider
from src.ui.text_input import TextInput
from src.utils import assets
from src.utils import codes
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui.image_button import _ImageButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

class SettingsState(GameState):
    """Settings screen with sound control and code redemption"""
    
    def __init__(self, game: 'Game'):
        """
        Initialize the settings state
        
        Args:
            game: Reference to the main Game instance
        """
        super().__init__(game)
        self.background = None
        self.sound_slider = None
        self.save_button = None
        self.logout_button = None
        self.font_title = None
        self.font_normal = None
        self.font_small = None
        
        # Message display
        self.message = ""
        self.message_color = (255, 255, 255)
        self.message_timer = 0
        self.message_duration = 3.0  # seconds
    
    def enter(self):
        """เรียกเมื่อเข้าสู่หน้านี้ - โหลดรูปภาพและสร้าง UI"""
        # โหลดพื้นหลัง town_2
        try:
            self.background = assets.load_image('assets/backgrounds/town_2.png', 
                                                     (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Warning: Could not load background: {e}")
            # สร้างพื้นหลังสำรอง
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((40, 30, 20))
        
        # Load fonts
        try:
            self.font_title = assets.load_font('assets/fonts/Monocraft.ttf', 48)
            self.font_normal = assets.load_font('assets/fonts/Monocraft.ttf', 24)
            self.font_small = assets.load_font('assets/fonts/Monocraft.ttf', 20)
        except Exception as e:
            print(f"Warning: Could not load font: {e}")

        # ตำแหน่งและขนาด
        center_x = SCREEN_WIDTH // 2
        start_y = 250
        
        # ดึงค่า volume เริ่มต้น (ถ้ามี player_data)
        initial_volume = 50  # ค่าเริ่มต้น
        if hasattr(self.game, 'player_data') and self.game.player_data:
            initial_volume = self.game.player_data['settings'].get('volume', 50)
        
        # Sound slider (แถบปรับเสียง - เล็กลง)
        self.sound_slider = Slider(
            x=center_x - 100,
            y=start_y,
            width=200,
            height=15,
            min_value=0,
            max_value=100,
            initial_value=initial_volume,
            callback=self.on_sound_change,
            label="Volume:",
            font=self.font_small
        )
        
        # โหลดรูปปุ่ม (ใช้รูปเดียวกับหน้าแรก)
        try:
            button_img = assets.load_image('assets/ui/12.png').convert_alpha()
            button_save = assets.load_image('assets/ui/save_button.png').convert_alpha()
            button_logout = assets.load_image('assets/ui/logout.png').convert_alpha()
        except Exception as e:
            print(f"Warning: Could not load button image: {e}")
            button_img = pygame.Surface((220, 70), pygame.SRCALPHA)
            button_img.fill((60, 60, 90, 255))
            pygame.draw.rect(button_img, (255, 255, 255, 40), button_img.get_rect(), border_radius=16)
        
        # ปุ่ม LOGOUT (ใต้แถบเสียง)
        logout_y = SCREEN_HEIGHT - 60
        self.logout_button = _ImageButton(
            button_logout,
            center=(center_x, logout_y),
            on_click=self.on_logout_click,
            scale=0.8,
            use_mask=True,
        )
        
        # ปุ่ม SAVE (วางไว้ล่างสุด ใช้ _ImageButton เหมือนหน้าแรก)
        button_center_y = start_y + 100  # วางล่างสุด
        self.save_button = _ImageButton(
            button_save,
            center=(center_x, button_center_y),
            on_click=self.on_save_click,
            scale=0.8,
            use_mask=True,
        )
    
    def on_sound_change(self, value):
        """
        Callback for sound slider - adjust game volume
        
        Args:
            value: New volume value (0-100)
        """
        # Update player settings (ถ้ามี player_data)
        if hasattr(self.game, 'player_data') and self.game.player_data:
            self.game.player_data['settings']['volume'] = value
        
        # Adjust pygame mixer volume (0.0 to 1.0)
        volume = value / 100.0
        
        # ใช้ method ของ game
        if hasattr(self.game, 'set_music_volume'):
            self.game.set_music_volume(volume)
        else:
            # fallback
            try:
                pygame.mixer.music.set_volume(volume)
            except:
                pass
        
        print(f"Volume adjusted to: {int(value)}%")
    
    def on_logout_click(self):
        """เมื่อกดปุ่ม LOGOUT - บันทึกและกลับไปหน้า loading"""
        print("Logout button clicked - saving and returning to loading")
        # บันทึกการตั้งค่า
        if hasattr(self.game, 'current_player_slot') and self.game.current_player_slot is not None:
            self.game.save_game()
        
        # กลับไปหน้า loading
        self.game.change_state('loading')
    
    def on_save_click(self):
        """เมื่อกดปุ่ม SAVE - บันทึกการตั้งค่าและกลับไปหน้าเดิม"""
        print("Save button clicked - saving settings")
        # บันทึกการตั้งค่า (ถ้ามีผู้เล่นเลือกแล้ว)
        if hasattr(self.game, 'current_player_slot') and self.game.current_player_slot is not None:
            self.game.save_game()
        
        # กลับไปหน้าเดิม (loading หรือ main_lobby)
        if hasattr(self.game, 'previous_state') and self.game.previous_state:
            self.game.change_state(self.game.previous_state)
        else:
            self.game.change_state('loading')
    
    def show_message(self, text, color=(255, 255, 255)):
        """
        Display a temporary message
        
        Args:
            text: Message text
            color: Message color
        """
        self.message = text
        self.message_color = color
        self.message_timer = self.message_duration
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: pygame.event.Event object
        """
        # ส่งต่อ event ไปยัง UI
        if self.sound_slider:
            self.sound_slider.handle_event(event)
        if self.logout_button:
            self.logout_button.handle_event(event)
        if self.save_button:
            self.save_button.handle_event(event)
    
    def update(self, dt):
        """
        Update game state logic
        
        Args:
            dt: Delta time in seconds since last update
        """
        # อัปเดต UI
        if self.sound_slider:
            self.sound_slider.update()
        if self.logout_button:
            self.logout_button.update(dt)
        if self.save_button:
            self.save_button.update(dt)
        
        # Update message timer
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""
    
    def draw(self, screen):
        """
        Draw the settings state to the screen
        
        Args:
            screen: pygame.Surface to draw on
        """
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
        
        # วาดหัวข้อ SETTING
        if self.font_title:
            title_surface = self.font_title.render("SETTING", True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
            screen.blit(title_surface, title_rect)
        
        # วาด UI (แถบปรับเสียง, ปุ่ม LOGOUT และปุ่ม SAVE)
        if self.sound_slider:
            self.sound_slider.draw(screen)
        if self.logout_button:
            self.logout_button.draw(screen)
        if self.save_button:
            self.save_button.draw(screen)
        
        # Draw message if active
        if self.message and self.message_timer > 0:
            if self.font_normal:
                message_surface = self.font_normal.render(self.message, True, self.message_color)
                message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, 450))
                
                # Draw semi-transparent background for message
                bg_rect = message_rect.inflate(20, 10)
                bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
                bg_surface.fill((0, 0, 0))
                bg_surface.set_alpha(180)
                screen.blit(bg_surface, bg_rect)
                
                screen.blit(message_surface, message_rect)
    
    def exit(self):
        """Called when exiting this state"""
        pass