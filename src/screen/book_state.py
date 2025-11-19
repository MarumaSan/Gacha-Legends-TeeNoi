"""Book state - หน้า Collection แสดงตัวละคร 2 ตัวต่อหน้า"""

import pygame
from src.core.game_state import GameState
from src.utils import assets
from src.ui.image_button import _ImageButton

from src.data.hero_data import get_all_heroes, Character
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

class BookState(GameState):
    """หน้า Collection - แสดงตัวละคร 2 ตัวต่อหน้า"""
    
    # States
    STATE_LIST = "list"  # แสดงรายการตัวละคร
    STATE_INFO = "info"  # แสดงข้อมูลตัวละคร
    
    def __init__(self, game: 'Game', player_data):
        super().__init__(game)
        self.player_data = player_data
        
        self.background = None
        self.font_title = None
        self.font_normal = None
        self.font_small = None
        
        # ปุ่ม
        self.left_button = None
        self.right_button = None
        self.back_button = None
        self.info_back_button = None  # ปุ่ม BACK ในหน้า info
        
        # ข้อมูลตัวละคร
        self.all_heroes = []
        self.current_page = 0  # หน้าปัจจุบัน (แต่ละหน้าแสดง 2 ตัว)
        self.heroes_per_page = 2
        
        # สถานะและข้อมูลที่เลือก
        self.current_state = self.STATE_LIST
        self.selected_hero: Character = None  # ตัวละครที่เลือกดู
        self.hero_rects = []  # rect สำหรับตรวจจับการคลิก
    
    def enter(self):
        """เรียกเมื่อเข้าสู่หน้านี้"""
        # โหลดพื้นหลัง
        try:
            self.background = assets.load_image('assets/backgrounds/book.png', (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Warning: Could not load background: {e}")
        
        # โหลดฟอนต์
        try:
            self.font_title = assets.load_font('assets/fonts/Monocraft.ttf', 25)
            self.font_normal = assets.load_font('assets/fonts/Monocraft.ttf', 18)
            self.font_small = assets.load_font('assets/fonts/Monocraft.ttf', 12)
        except Exception as e:
            print(f"Warning: Could not load font: {e}")
            self.font_title = pygame.font.Font(None, 32)
            self.font_normal = pygame.font.Font(None, 20)
            self.font_small = pygame.font.Font(None, 12)
        
        # โหลดและเรียงตัวละครทั้งหมดตาม id (จากน้อยไปมาก)
        all_heroes_raw = get_all_heroes()
        self.all_heroes = sorted(all_heroes_raw, key=lambda hero: hero.id)
        
        # โหลดรูปปุ่ม
        try:
            left_img = assets.load_image('assets/ui/left botton.png')
            right_img = assets.load_image('assets/ui/right botton.png')
            lobby_img = assets.load_image('assets/ui/12.png').convert_alpha()
        except Exception as e:
            print(f"Warning: Could not load button images: {e}")
            left_img = pygame.Surface((60, 60), pygame.SRCALPHA)
            right_img = pygame.Surface((60, 60), pygame.SRCALPHA)
            lobby_img = pygame.Surface((220, 70), pygame.SRCALPHA)
            left_img.fill((100, 80, 60, 200))
            right_img.fill((100, 80, 60, 200))
            lobby_img.fill((60, 60, 90, 255))
        
        # ปุ่มซ้าย (เปลี่ยนหน้าก่อนหน้า)
        self.left_button = _ImageButton(
            left_img,
            center=(100, SCREEN_HEIGHT // 2),
            on_click=self.on_prev_page,
            scale=1.0,
            use_mask=True
        )
        
        # ปุ่มขวา (เปลี่ยนหน้าถัดไป)
        self.right_button = _ImageButton(
            right_img,
            center=(SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2),
            on_click=self.on_next_page,
            scale=1.0,
            use_mask=True
        )
        
        # ปุ่ม RETURN TO LOBBY
        self.back_button = _ImageButton(
            lobby_img,
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60),
            on_click=self.on_back_click,
            scale=1.5,
            use_mask=True,
            text="RETURN TO LOBBY",
            font=self.font_small
        )
        
        # ปุ่ม BACK (ในหน้า info)
        self.info_back_button = _ImageButton(
            lobby_img,
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60),
            on_click=self.on_info_back_click,
            scale=1.2,
            use_mask=True,
            text="BACK",
            font=self.font_small
        )
        
        # รีเซ็ตสถานะ
        self.current_state = self.STATE_LIST
        self.selected_hero = None
    
    def on_prev_page(self):
        """ไปหน้าก่อนหน้า"""
        if self.current_page > 0:
            self.current_page -= 1
    
    def on_next_page(self):
        """ไปหน้าถัดไป"""
        max_page = (len(self.all_heroes) - 1) // self.heroes_per_page
        if self.current_page < max_page:
            self.current_page += 1
    
    def on_back_click(self):
        """กลับไปหน้า lobby"""
        self.game.change_state('main_lobby')
    
    def on_info_back_click(self):
        """กลับจากหน้า info ไปหน้า list"""
        self.current_state = self.STATE_LIST
        self.selected_hero = None
    
    def handle_event(self, event):
        """จัดการ event"""
        if self.current_state == self.STATE_LIST:
            # หน้ารายการ
            if self.left_button:
                self.left_button.handle_event(event)
            if self.right_button:
                self.right_button.handle_event(event)
            if self.back_button:
                self.back_button.handle_event(event)
            
            # ตรวจจับการคลิกที่ตัวละคร
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                for rect, hero in self.hero_rects:
                    if rect.collidepoint(mouse_pos):
                        # คลิกที่ตัวละคร - เปิดหน้า info
                        self.selected_hero = hero
                        self.current_state = self.STATE_INFO
                        break
        
        elif self.current_state == self.STATE_INFO:
            # หน้าข้อมูล
            if self.info_back_button:
                self.info_back_button.handle_event(event)
    
    def update(self, dt):
        """อัปเดตสถานะ"""
        if self.current_state == self.STATE_LIST:
            if self.left_button:
                self.left_button.update(dt)
            if self.right_button:
                self.right_button.update(dt)
            if self.back_button:
                self.back_button.update(dt)
        elif self.current_state == self.STATE_INFO:
            if self.info_back_button:
                self.info_back_button.update(dt)
    
    def draw(self, screen):
        """วาดหน้าจอ"""
        # วาดพื้นหลัง
        if self.background:
            screen.blit(self.background, (0, 0))
        
        if self.current_state == self.STATE_LIST:
            self._draw_list(screen)
        elif self.current_state == self.STATE_INFO:
            self._draw_info(screen)
    
    def _draw_list(self, screen: pygame.Surface):
        """วาดหน้ารายการตัวละคร"""
        # คำนวณตัวละครที่จะแสดงในหน้านี้
        start_idx = self.current_page * self.heroes_per_page
        end_idx = min(start_idx + self.heroes_per_page, len(self.all_heroes))
        current_heroes = self.all_heroes[start_idx:end_idx]
        
        # ล้าง hero_rects
        self.hero_rects = []
        
        # วาดตัวละคร 2 ตัว (ซ้ายและขวา - ขยับเข้ามาตรงกลาง 130px)
        for i, hero in enumerate(current_heroes):
            # ตำแหน่ง (ซ้าย = 1/4 หน้าจอ + 130, ขวา = 3/4 หน้าจอ - 130)
            if i == 0:
                x = SCREEN_WIDTH // 4 + 130
            else:
                x = SCREEN_WIDTH * 3 // 4 - 130
            
            y = SCREEN_HEIGHT // 2 - 50
            
            # ตรวจสอบว่าผู้เล่นมีตัวละครนี้หรือไม่
            is_owned = hero.id in self.player_data['owned_heroes']
            
            # โหลดและแสดงรูปตัวละคร
            try:
                portrait = assets.load_image(hero.portrait_path)
                
                original_width = portrait.get_width()
                original_height = portrait.get_height()
                max_height = 300
                scale = max_height / original_height
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)
                portrait_scaled = pygame.transform.smoothscale(portrait, (new_width, new_height))
                
                # ถ้ายังไม่มี - แปลงเป็นขาวดำ
                if not is_owned:
                    # แปลงเป็น grayscale โดยรักษาความโปร่งใส
                    grayscale = pygame.Surface(portrait_scaled.get_size(), pygame.SRCALPHA)
                    for px in range(new_width):
                        for py in range(new_height):
                            color = portrait_scaled.get_at((px, py))
                            gray = int(0.299 * color.r + 0.587 * color.g + 0.114 * color.b)
                            grayscale.set_at((px, py), (gray, gray, gray, color.a))
                    portrait_scaled = grayscale
                
                # วาดตรงกลาง
                portrait_x = x - new_width // 2
                portrait_y = y - new_height // 2 + 20
                screen.blit(portrait_scaled, (portrait_x, portrait_y))
                
                # เก็บ rect สำหรับตรวจจับการคลิก
                hero_rect = pygame.Rect(portrait_x, portrait_y, new_width, new_height)
                self.hero_rects.append((hero_rect, hero))

            except Exception as e:
                print(f"Warning: Could not load portrait: {e}")
            
            hero_name_color = {
            'rare' :  (18, 97, 160),
            'epic' : (203, 108, 230),
            'legendary' : (228, 162, 31),
            'extreme' : (255,82,82)
            }
            # แสดงชื่อตัวละคร
            if self.font_normal:
                if is_owned:
                    name_text = self.font_normal.render(hero.name, True, (0, 0, 0))
                    rarity_text = self.font_small.render(f'[{hero.rarity}]', True, hero_name_color[hero.rarity])
                else:
                    name_text = self.font_normal.render("???", True, (100, 100, 100))
                    rarity_text = self.font_small.render(f'[???]', True, (100, 100, 100))

                screen.blit(name_text, (x - name_text.get_width() // 2, y - 175))
                screen.blit(rarity_text, (x - rarity_text.get_width() // 2, y - 155))
        
        # วาดปุ่ม (ในหน้า list)
        if self.left_button:
            self.left_button.draw(screen)
        if self.right_button:
            self.right_button.draw(screen)
        if self.back_button:
            self.back_button.draw(screen)
    
    def _draw_info(self, screen: pygame.Surface):
        """วาดหน้าข้อมูลตัวละคร"""
        if not self.selected_hero:
            return
        
        hero = self.selected_hero
        is_owned = hero.id in self.player_data['owned_heroes']
        
        # ซ้าย - รูปตัวละคร (ขยับเข้ามา 120px และขึ้น 20px)
        left_x = SCREEN_WIDTH // 4 + 120
        center_y = SCREEN_HEIGHT // 2 - 20
        
        try:
            portrait = assets.load_image(hero.portrait_path)

            original_width = portrait.get_width()
            original_height = portrait.get_height()
            max_height = 350
            scale = max_height / original_height
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            portrait_scaled = pygame.transform.smoothscale(portrait, (new_width, new_height))
            
            # ถ้ายังไม่มี - แปลงเป็นขาวดำ
            if not is_owned:
                grayscale = pygame.Surface(portrait_scaled.get_size(), pygame.SRCALPHA)
                for px in range(new_width):
                    for py in range(new_height):
                        color = portrait_scaled.get_at((px, py))
                        gray = int(0.299 * color.r + 0.587 * color.g + 0.114 * color.b)
                        grayscale.set_at((px, py), (gray, gray, gray, color.a))
                portrait_scaled = grayscale
            
            # วาด
            portrait_x = left_x - new_width // 2
            portrait_y = center_y - new_height // 2
            screen.blit(portrait_scaled, (portrait_x, portrait_y))
        except:
            pass
        
        # ขวา - ข้อมูลตัวละคร
        right_x = SCREEN_WIDTH * 3 // 4 - 125
        start_y = 200
        line_spacing = 50
        hero_name_color = {
            'rare' :  (18, 97, 160),
            'epic' : (203, 108, 230),
            'legendary' : (228, 162, 31),
            'extreme' : (255,82,82)
        }
        
        if self.font_title:
            # ชื่อ
            if is_owned:
                name = self.font_title.render(hero.name, True, hero_name_color[hero.rarity])
            else:
                name = self.font_title.render("???", True, hero_name_color[hero.rarity])
                
            screen.blit(name, (right_x - name.get_width() // 2, start_y))
        
        if self.font_normal and is_owned:
            # Rarity
            rarity_text = f"RARITY : {hero.rarity.upper()}"
            rarity = self.font_normal.render(rarity_text, True, (85,85,85))
            screen.blit(rarity, (right_x - rarity.get_width() // 2, start_y + line_spacing))
            
            # ATK
            atk_text = f"ATK : {hero.atk}"
            atk = self.font_normal.render(atk_text, True, (85,85,85))
            screen.blit(atk, (right_x - atk.get_width() // 2, start_y + line_spacing * 2))
            
            # DEF
            def_text = f"DEF : {hero.defense}"
            def_render = self.font_normal.render(def_text, True, (85,85,85))
            screen.blit(def_render, (right_x - def_render.get_width() // 2, start_y + line_spacing * 3))
            
            # POWER
            power_text = f"POWER : {hero.totalPower}"
            power = self.font_normal.render(power_text, True, (85,85,85))
            screen.blit(power, (right_x - power.get_width() // 2, start_y + line_spacing * 4))
        
        else:
            rarity_text = f"RARITY : ???"
            rarity = self.font_normal.render(rarity_text, True, (85,85,85))
            screen.blit(rarity, (right_x - rarity.get_width() // 2, start_y + line_spacing))
            
            # ATK
            atk_text = f"ATK : ???"
            atk = self.font_normal.render(atk_text, True, (85,85,85))
            screen.blit(atk, (right_x - atk.get_width() // 2, start_y + line_spacing * 2))
            
            # DEF
            def_text = f"DEF : ???"
            def_render = self.font_normal.render(def_text, True, (85,85,85))
            screen.blit(def_render, (right_x - def_render.get_width() // 2, start_y + line_spacing * 3))
            
            # POWER
            power_text = f"POWER : ???"
            power = self.font_normal.render(power_text, True, (85,85,85))
            screen.blit(power, (right_x - power.get_width() // 2, start_y + line_spacing * 4))
        
        # ปุ่ม BACK
        if self.info_back_button:
            self.info_back_button.draw(screen)
    
    def exit(self):
        """เรียกเมื่อออกจากหน้านี้"""
        pass
