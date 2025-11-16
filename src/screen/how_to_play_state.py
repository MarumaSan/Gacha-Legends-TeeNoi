"""How to Play state - หน้าแสดงวิธีเล่น"""

import pygame
from src.core.game_state import GameState
from src.utils import assets
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT


def _color_effect(src: pygame.Surface, mul=(230, 230, 230, 255)) -> pygame.Surface:
    """สร้าง effect สีให้กับรูปภาพ"""
    img = src.copy()
    img.fill(mul, special_flags=pygame.BLEND_RGBA_MULT)
    return img


class _ImageButton:
    """ปุ่มที่ใช้รูปภาพพร้อม hover effect"""
    def __init__(self, base_img: pygame.Surface, center, on_click=None, scale=1.0, use_mask=True, text="", font=None):
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


class HowToPlayState(GameState):
    """หน้าแสดงวิธีเล่น - มีรูป 17 หน้า"""
    
    def __init__(self, game):
        super().__init__(game)
        
        self.current_page = 1  # หน้าปัจจุบัน (1-17)
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
            print(f"Previous page: {self.current_page}")
    
    def on_next_page(self):
        """ไปหน้าถัดไป หรือกลับไปหน้า loading ถ้าถึงหน้าสุดท้าย"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            print(f"Next page: {self.current_page}")
        else:
            # ถึงหน้าสุดท้ายแล้ว กลับไปหน้า loading
            print("End of tutorial - returning to loading")
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
