"""Add Code state - หน้ากรอกโค้ดเพื่อรับรางวัล"""

import pygame
from src.core.game_state import GameState
from src.utils import assets
from src.utils import codes
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui.image_button import _ImageButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game



class AddCodeState(GameState):
    """หน้ากรอกโค้ดเพื่อรับรางวัล"""
    
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.player_slot = 1  # จะถูกตั้งค่าใน enter()
        self.background = None
        self.font_title = None
        self.font_large = None
        self.font_normal = None
        self.font_small = None
        
        # UI elements
        self.code_frame = None  # กรอบสำหรับกรอกโค้ด
        self.code_input_rect = None  # พื้นที่สำหรับกรอกโค้ด
        self.code_text = ""  # ข้อความโค้ดที่กรอก
        self.done_button = None  # ปุ่ม DONE
        self.back_button = None  # ปุ่ม RETURN TO LOBBY
        
        # Message display
        self.message = ""
        self.message_color = (255, 255, 255)
        self.message_timer = 0
        self.message_duration = 3.0
        
        # Input state
        self.input_active = True  # ช่องกรอกโค้ดเปิดใช้งานอยู่เสมอ
    
    def enter(self):
        """เรียกเมื่อเข้าสู่หน้านี้ - โหลดรูปภาพและสร้าง UI"""
        # เก็บ player_slot สำหรับใช้ในการ redeem code
        if hasattr(self.game, 'current_player_slot'):
            self.player_slot = self.game.current_player_slot
        else:
            self.player_slot = 1
        
        # โหลดพื้นหลัง summon_2.png
        try:
            self.background = assets.load_image('assets/backgrounds/summon_2.png', 
                                                     (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Warning: Could not load background: {e}")
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((40, 30, 20))
        
        # โหลดฟอนต์
        try:
            self.font_title = assets.load_font('assets/fonts/Monocraft.ttf', 60)
            self.font_large = assets.load_font('assets/fonts/Monocraft.ttf', 32)  # สำหรับแสดงรางวัล
            self.font_normal = assets.load_font('assets/fonts/Monocraft.ttf', 20)
            self.font_small = assets.load_font('assets/fonts/Monocraft.ttf', 12)
        except Exception as e:
            print(f"Warning: Could not load font: {e}")
            self.font_title = pygame.font.Font(None, 32)
            self.font_large = pygame.font.Font(None, 32)
            self.font_normal = pygame.font.Font(None, 20)
            self.font_small = pygame.font.Font(None, 15)
        
        # โหลดกรอบโค้ด frame code.png
        try:
            self.code_frame = assets.load_image('assets/ui/frame code.png')
        except Exception as e:
            print(f"Warning: Could not load code frame: {e}")
            # สร้างกรอบสำรอง
            self.code_frame = pygame.Surface((400, 60), pygame.SRCALPHA)
            self.code_frame.fill((100, 80, 60, 200))
            pygame.draw.rect(self.code_frame, (200, 180, 150), self.code_frame.get_rect(), 3)
        
        # ตำแหน่งกรอบโค้ด (ตรงกลาง)
        frame_x = SCREEN_WIDTH // 2 - self.code_frame.get_width() // 2
        frame_y = SCREEN_HEIGHT // 2 - 50
        self.code_input_rect = pygame.Rect(frame_x, frame_y, 
                                           self.code_frame.get_width(), 
                                           self.code_frame.get_height())
        
        # โหลดรูปปุ่ม
        try:
            button_img = assets.load_image('assets/ui/12.png').convert_alpha()
        except Exception as e:
            print(f"Warning: Could not load button image: {e}")
            button_img = pygame.Surface((220, 70), pygame.SRCALPHA)
            button_img.fill((60, 60, 90, 255))
            pygame.draw.rect(button_img, (255, 255, 255, 40), button_img.get_rect(), border_radius=16)
        
        # ปุ่ม DONE (อยู่ใต้กรอบโค้ด)
        done_y = frame_y + 100
        self.done_button = _ImageButton(
            button_img,
            center=(SCREEN_WIDTH // 2, done_y),
            on_click=self.on_done_click,
            scale=1.2,
            use_mask=True,
            text="DONE",
            font=self.font_small
        )
        
        # ปุ่ม RETURN TO LOBBY
        back_y = SCREEN_HEIGHT - 60
        self.back_button = _ImageButton(
            button_img,
            center=(SCREEN_WIDTH // 2, back_y),
            on_click=self.on_back_click,
            scale=1.5,
            use_mask=True,
            text="RETURN TO LOBBY",
            font=self.font_small
        )
    
    def on_done_click(self):
        """เมื่อกดปุ่ม DONE - ตรวจสอบและใช้โค้ด"""
        if not self.code_text:
            self.show_message("Please enter a code!", (255, 100, 100))
            return
        
        success, message, coins = codes.redeem_code(self.code_text, self.player_slot)
        
        if success:
            # โค้ดถูกต้อง - เพิ่มเหรียญให้ผู้เล่น
            from src.utils import player
            player.add_coins(self.game.player_data, coins)
            # แสดงจำนวนเหรียญที่ได้ (fade ขึ้นมาแล้วหายไป)
            reward_text = f"+{coins}"
            self.show_message(reward_text, (255, 215, 0))  # สีทอง
            self.code_text = ""  # ล้างช่องกรอก
            # บันทึกข้อมูล
            self.game.save_game()
            print(f"Code redeemed successfully! New balance: {self.game.player_data['coins']}")
        else:
            # โค้ดผิด - แสดง INVALID CODE (fade ขึ้นมาแล้วหายไป)
            print(f"Code redemption failed: {message}")
            self.show_message("INVALID CODE", (255, 100, 100))
            self.code_text = ""  # ล้างช่องกรอกให้กรอกใหม่
    
    def on_back_click(self):
        """เมื่อกดปุ่ม RETURN TO LOBBY - กลับไปหน้าล็อบบี้"""
        self.game.change_state('main_lobby')
    
    def show_message(self, text, color=(255, 255, 255)):
        """แสดงข้อความชั่วคราว"""
        self.message = text
        self.message_color = color
        self.message_timer = self.message_duration
    
    def handle_event(self, event):
        """จัดการ event ต่างๆ"""
        # จัดการการพิมพ์ข้อความ
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.code_text = self.code_text[:-1]
            elif event.key == pygame.K_RETURN:
                self.on_done_click()
            elif len(self.code_text) < 20:  # จำกัดความยาว
                if event.unicode.isprintable():
                    self.code_text += event.unicode.upper()
        
        # จัดการปุ่ม
        if self.done_button:
            self.done_button.handle_event(event)
        if self.back_button:
            self.back_button.handle_event(event)
    
    def update(self, dt):
        """อัปเดตสถานะ"""
        # อัปเดตปุ่ม
        if self.done_button:
            self.done_button.update(dt)
        if self.back_button:
            self.back_button.update(dt)
        
        # อัปเดต message timer
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.message = ""
    
    def draw(self, screen):
        """วาดหน้าจอ"""
        # วาดพื้นหลัง
        if self.background:
            screen.blit(self.background, (0, 0))
        
        # วาดหัวข้อ REDEEM CODE
        if self.font_title:
            title = self.font_title.render("REDEEM CODE", True, (255, 255, 255))
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        
        # วาดกรอบโค้ด
        if self.code_frame and self.code_input_rect:
            screen.blit(self.code_frame, self.code_input_rect)
            
            # วาดข้อความที่กรอก
            if self.font_normal:
                code_surface = self.font_normal.render(self.code_text, True, (100, 200, 255))
                code_rect = code_surface.get_rect(center=self.code_input_rect.center)
                screen.blit(code_surface, code_rect)
        
        # วาดปุ่ม DONE
        if self.done_button:
            self.done_button.draw(screen)
        
        # วาดปุ่ม RETURN TO LOBBY
        if self.back_button:
            self.back_button.draw(screen)
        
        # วาดข้อความแจ้งเตือน (fade in/out effect)
        if self.message and self.message_timer > 0:
            if self.font_large:
                # คำนวณ alpha สำหรับ fade effect
                # fade in ครึ่งแรก, fade out ครึ่งหลัง
                progress = self.message_timer / self.message_duration
                if progress > 0.5:
                    # ครึ่งแรก - fade in
                    alpha = int(255 * (1 - progress) * 2)
                else:
                    # ครึ่งหลัง - fade out
                    alpha = int(255 * progress * 2)
                
                # วาดข้อความขนาดใหญ่ตรงกลางจอ
                msg_surface = self.font_large.render(self.message, True, self.message_color)
                msg_surface.set_alpha(alpha)
                msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150))
                
                screen.blit(msg_surface, msg_rect)
    
    def exit(self):
        """เรียกเมื่อออกจากหน้านี้"""
        pass
