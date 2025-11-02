"""Settings state - game settings and code redemption"""

import pygame
from file_game.code.game_state import GameState
from file_game.code.ui.button import Button
from file_game.code.ui.slider import Slider
from file_game.code.ui.text_input import TextInput
from file_game.code.system.asset_manager import AssetManager
from file_game.code.system.code_manager import CodeManager
from file_game.code.config import SCREEN_WIDTH, SCREEN_HEIGHT


def _color_effect(src: pygame.Surface, mul=(230, 230, 230, 255)) -> pygame.Surface:
    img = src.copy()
    img.fill(mul, special_flags=pygame.BLEND_RGBA_MULT)
    return img


class _ImageButton:
    def __init__(self, base_img: pygame.Surface, center, on_click=None, scale=1.2, use_mask=True, text="", font=None):
        if scale != 1.0:
            w, h = base_img.get_size()
            base_img = pygame.transform.smoothscale(base_img, (int(w * scale), int(h * scale)))

        self.normal = base_img
        self.hover = _color_effect(base_img, (230, 240, 245, 255))
        self.down = _color_effect(base_img, (200, 200, 200, 255))

        self.image = self.normal
        self.rect = self.image.get_rect(center=center)

        self.on_click = on_click
        self._held = False
        self._over = False

        self.use_mask = use_mask
        self.mask = pygame.mask.from_surface(self.image) if use_mask else None

        self.text = text
        self.font = font
        self.text_color = (255, 255, 255)

    def _hit(self, pos):
        if not self.rect.collidepoint(pos):
            return False
        if not self.use_mask:
            return True
        lx, ly = pos[0] - self.rect.x, pos[1] - self.rect.y
        return bool(self.mask.get_at((lx, ly)))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._hit(event.pos):
                self._held = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._held and self._hit(event.pos):
                if self.on_click:
                    self.on_click()
            self._held = False

    def update(self, dt):
        mpos = pygame.mouse.get_pos()
        self._over = self._hit(mpos)

        if self._over and self._held:
            self.image = self.down
        elif self._over:
            self.image = self.hover
        else:
            self.image = self.normal

    def draw(self, surf):
        shadow = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 60),
                            (0, int(self.rect.height * 0.75), self.rect.width, int(self.rect.height * 0.5)))
        surf.blit(shadow, (self.rect.x, self.rect.y))
        surf.blit(self.image, self.rect)

        if self.text and self.font:
            label = self.font.render(self.text, True, self.text_color)
            surf.blit(label, label.get_rect(center=self.rect.center))


class SettingsState(GameState):
    """Settings screen with sound control and code redemption"""
    
    def __init__(self, game):
        """
        Initialize the settings state
        
        Args:
            game: Reference to the main Game instance
        """
        super().__init__(game)
        self.assets = AssetManager()
        self.code_manager = CodeManager()
        self.background = None
        self.sound_slider = None
        self.save_button = None
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
            self.background = self.assets.load_image('assets/backgrounds/town_2.png', 
                                                     (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Warning: Could not load background: {e}")
            # สร้างพื้นหลังสำรอง
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((40, 30, 20))
        
        # Load fonts
        try:
            self.font_title = self.assets.load_font('assets/fonts/Monocraft.ttf', 48)
            self.font_normal = self.assets.load_font('assets/fonts/Monocraft.ttf', 24)
            self.font_small = self.assets.load_font('assets/fonts/Monocraft.ttf', 20)
        except Exception as e:
            print(f"Warning: Could not load font: {e}")
            self.font_title = pygame.font.Font(None, 48)
            self.font_normal = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 20)
        
        # ตำแหน่งและขนาด
        center_x = SCREEN_WIDTH // 2
        start_y = 250
        
        # Sound slider (แถบปรับเสียง - เล็กลง)
        self.sound_slider = Slider(
            x=center_x - 100,
            y=start_y,
            width=200,
            height=15,
            min_value=0,
            max_value=100,
            initial_value=self.game.player_data.settings.get('volume', 50),
            callback=self.on_sound_change,
            label="Volume:",
            font=self.font_small
        )
        
        # โหลดรูปปุ่ม (ใช้รูปเดียวกับหน้าแรก)
        try:
            button_img = self.assets.load_image('assets/ui/12.png').convert_alpha()
        except Exception as e:
            print(f"Warning: Could not load button image: {e}")
            button_img = pygame.Surface((220, 70), pygame.SRCALPHA)
            button_img.fill((60, 60, 90, 255))
            pygame.draw.rect(button_img, (255, 255, 255, 40), button_img.get_rect(), border_radius=16)
        
        # ปุ่ม SAVE (วางไว้ล่างสุด ใช้ _ImageButton เหมือนหน้าแรก)
        button_center_y = SCREEN_HEIGHT - 60  # วางล่างสุด
        self.save_button = _ImageButton(
            button_img,
            center=(center_x, button_center_y),
            on_click=self.on_save_click,
            scale=1.2,
            use_mask=True,
            text="SAVE",
            font=self.font_normal
        )
    
    def on_sound_change(self, value):
        """
        Callback for sound slider - adjust game volume
        
        Args:
            value: New volume value (0-100)
        """
        # Update player settings
        self.game.player_data.settings['volume'] = value
        
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
    
    def on_save_click(self):
        """เมื่อกดปุ่ม SAVE - บันทึกการตั้งค่าและกลับไปหน้า main lobby"""
        print("Save button clicked - saving settings")
        # บันทึกการตั้งค่า
        self.game.save_game()
        # กลับไปหน้า main lobby
        self.game.change_state('main_lobby')
    
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
        
        # วาด UI (แถบปรับเสียงและปุ่ม SAVE)
        if self.sound_slider:
            self.sound_slider.draw(screen)
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