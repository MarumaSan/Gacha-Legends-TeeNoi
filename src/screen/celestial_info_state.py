"""Celestial Info state - แสดงตัวละครและ rate ที่สุ่มได้จาก Celestial Chest"""

import pygame
from src.core.game_state import GameState
from src.utils import assets
from src.data.hero_data import get_heroes_by_rarity
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT


def _color_effect(src: pygame.Surface, mul=(230, 230, 230, 255)) -> pygame.Surface:
    """สร้าง effect สีให้กับรูปภาพ"""
    img = src.copy()
    img.fill(mul, special_flags=pygame.BLEND_RGBA_MULT)
    return img


class _ImageButton:
    """ปุ่มที่ใช้รูปภาพพร้อม hover effect"""
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


class CelestialInfoState(GameState):
    """หน้าแสดงข้อมูล Celestial Chest - ตัวละครและ rate"""
    
    def __init__(self, game):
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
            'extreme': 0.01,    # 1%
            'legendary': 0.04,  # 4%
            'epic': 0.25,       # 25%
            'rare': 0.70        # 70%
        }
        
        # สีของแต่ละ rarity
        self.rarity_colors = {
            'extreme': (255, 0, 255),      # ชมพูสด
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
        
        for rarity in ['extreme', 'legendary', 'epic', 'rare']:
            heroes = self.heroes_by_rarity.get(rarity, [])
            rate = self.rates[rarity]
            color = self.rarity_colors[rarity]
            
            # หัวข้อ rarity และ rate
            if self.font_normal:
                rarity_text = f"{rarity.upper()} - {rate*100:.0f}%"
                rarity_surf = self.font_normal.render(rarity_text, True, color)
                screen.blit(rarity_surf, (50, start_y))
            
            # แสดงการ์ดตัวละคร
            card_y = start_y + 30
            card_x = 50
            card_spacing = 10
            
            for i, hero in enumerate(heroes):
                # จำกัดแสดงไม่เกิน 10 ตัวต่อแถว
                if i >= 10:
                    break
                
                try:
                    card_img = assets.load_image(hero.card_front_path, (60, 84))
                    screen.blit(card_img, (card_x + i * (60 + card_spacing), card_y))
                except Exception as e:
                    # สร้างการ์ดสำรอง
                    fallback = pygame.Surface((60, 84))
                    fallback.fill(color)
                    screen.blit(fallback, (card_x + i * (60 + card_spacing), card_y))
            
            start_y += 130
        
        # ปุ่ม BACK
        if self.back_button:
            self.back_button.draw(screen)
    
    def exit(self):
        """เรียกเมื่อออกจากหน้านี้"""
        pass
