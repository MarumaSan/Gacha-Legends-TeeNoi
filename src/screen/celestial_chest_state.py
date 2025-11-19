"""Celestial Chest state - หน้าสุ่ม Celestial Chest (มี EXTREME)"""

import pygame
import random
from src.core.game_state import GameState
from src.utils import assets, player
from src.data.hero_data import get_heroes_by_rarity, get_hero
from src.ui.animation import CardFlipAnimation
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT, SUMMON_COSTS, ASSET_PATHS
from src.ui.image_button import _ImageButton

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game

class CelestialChestState(GameState):
    """หน้าสุ่ม Celestial Chest (มี EXTREME)"""
    
    # States
    STATE_SELECTION = "selection"  # เลือกสุ่ม x1 หรือ x10
    STATE_REVEALING = "revealing"  # กำลังเปิดการ์ด
    STATE_NEW_HERO = "new_hero"  # แสดงฮีโร่ใหม่
    STATE_RESULTS = "results"  # แสดงผลลัพธ์ทั้งหมด
    
    def __init__(self, game: 'Game', player_data):
        super().__init__(game)
        self.player_data = player_data
        
        self.background = None
        self.font_title = None
        self.font_large = None
        self.font_normal = None
        self.font_small = None
        
        # ปุ่มในหน้าเลือก
        self.summon_x1_button = None
        self.summon_x10_button = None
        self.back_button = None
        self.question_button = None
        
        # ปุ่มในหน้าผลลัพธ์
        self.summon_again_button = None
        self.return_lobby_button = None
        
        # สถานะปัจจุบัน
        self.current_state = self.STATE_SELECTION
        
        # ข้อมูลการสุ่ม
        self.summoned_heroes = []  # ฮีโร่ที่สุ่มได้
        self.new_heroes = []  # ฮีโร่ใหม่ที่ไม่เคยมี
        self.current_new_hero_index = 0  # index ของฮีโร่ใหม่ที่กำลังแสดง
        
        # Animation เหรียญที่ถูกหัก
        self.coin_animations = []  # [(text, x, y, alpha, timer), ...]
        
        # การ์ด
        self.card_back_images = []  # รูปการ์ดหลังทั้งหมด (แต่ละใบอาจต่างกัน)
        self.card_front_images = []  # รูปการ์ดหน้าทั้งหมด
        self.card_positions = []  # ตำแหน่งการ์ดทั้งหมด
        self.revealed_cards = []  # การ์ดที่เปิดแล้ว (True/False)
        self.card_rects = []  # rect สำหรับตรวจจับการคลิก
        self.card_animations = []  # animation สำหรับแต่ละการ์ด
        
        # Hero pools (มี EXTREME)
        self.hero_pools = {
            'rare': get_heroes_by_rarity('rare'),
            'epic': get_heroes_by_rarity('epic'),
            'legendary': get_heroes_by_rarity('legendary'),
            'extreme': get_heroes_by_rarity('extreme')
        }
        
        # Celestial Chest rates (มี EXTREME)
        self.celestial_rates = {
            'rare': 0.70,      # 70%
            'epic': 0.25,      # 25%
            'legendary': 0.04, # 4%
            'extreme': 0.01    # 1%
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
            self.font_title = assets.load_font('assets/fonts/Monocraft.ttf', 48)
            self.font_large = assets.load_font('assets/fonts/Monocraft.ttf', 32)
            self.font_normal = assets.load_font('assets/fonts/Monocraft.ttf', 20)
            self.font_small = assets.load_font('assets/fonts/Monocraft.ttf', 12)
        except Exception as e:
            print(f"Warning: Could not load font: {e}")
            self.font_title = pygame.font.Font(None, 48)
            self.font_large = pygame.font.Font(None, 32)
            self.font_normal = pygame.font.Font(None, 20)
            self.font_small = pygame.font.Font(None, 15)
        
        # ไม่ต้องโหลดการ์ดหลังตอนนี้ เพราะจะโหลดตาม hero แต่ละตัว
        
        # สร้างปุ่มในหน้าเลือก
        self._create_selection_buttons()
        
        # รีเซ็ตสถานะ
        self.current_state = self.STATE_SELECTION
        self.summoned_heroes = []
        self.new_heroes = []
        self.current_new_hero_index = 0
    
    def _create_selection_buttons(self):
        """สร้างปุ่มในหน้าเลือกสุ่ม"""
        # โหลดรูปปุ่มสุ่ม (ใช้รูป premium)
        try:
            summon_x1_img = assets.load_image('assets/ui/summon premium1.png')
            summon_x10_img = assets.load_image('assets/ui/summon premium10.png')
        except Exception as e:
            print(f"Warning: Could not load summon images: {e}")
            summon_x1_img = pygame.Surface((150, 150), pygame.SRCALPHA)
            summon_x10_img = pygame.Surface((150, 150), pygame.SRCALPHA)
            summon_x1_img.fill((100, 80, 60, 200))
            summon_x10_img.fill((100, 80, 60, 200))
        
        # โหลดรูปปุ่ม
        try:
            button_img = assets.load_image('assets/ui/12.png').convert_alpha()
        except Exception as e:
            print(f"Warning: Could not load button image: {e}")
            button_img = pygame.Surface((220, 70), pygame.SRCALPHA)
            button_img.fill((60, 60, 90, 255))
        
        center_y = SCREEN_HEIGHT // 2 + 20
        spacing = 200
        
        self.summon_x1_button = _ImageButton(
            summon_x1_img,
            center=(SCREEN_WIDTH // 2 - spacing // 2, center_y),
            on_click=self.on_summon_x1_click,
            scale=1.0,
            use_mask=True
        )
        
        self.summon_x10_button = _ImageButton(
            summon_x10_img,
            center=(SCREEN_WIDTH // 2 + spacing // 2, center_y),
            on_click=self.on_summon_x10_click,
            scale=1.0,
            use_mask=True
        )
        
        self.back_button = _ImageButton(
            button_img,
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60),
            on_click=self.on_back_click,
            scale=1.5,
            use_mask=True,
            text="RETURN TO LOBBY",
            font=self.font_small
        )
        
        # โหลดรูปปุ่ม question
        try:
            question_img = assets.load_image('assets/ui/question.png', (50, 50))
        except Exception as e:
            print(f"Warning: Could not load question image: {e}")
            question_img = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(question_img, (255, 255, 255), (25, 25), 25)
            font = pygame.font.Font(None, 40)
            text = font.render("?", True, (0, 0, 0))
            question_img.blit(text, (15, 5))
        
        # ปุ่ม Question (มุมขวาบน)
        self.question_button = _ImageButton(
            question_img,
            center=(SCREEN_WIDTH - 40, 40),
            on_click=self.on_question_click,
            scale=1.0,
            use_mask=False
        )
    
    def _create_result_buttons(self):
        """สร้างปุ่มในหน้าผลลัพธ์"""
        try:
            button_img = assets.load_image('assets/ui/12.png').convert_alpha()
        except:
            button_img = pygame.Surface((220, 70), pygame.SRCALPHA)
            button_img.fill((60, 60, 90, 255))
        
        # สร้างฟอนต์เล็กพิเศษสำหรับปุ่ม
        try:
            button_font = assets.load_font('assets/fonts/Monocraft.ttf', 10)
        except:
            button_font = pygame.font.Font(None, 10)
        
        button_y = SCREEN_HEIGHT - 80
        spacing = 150
        
        self.summon_again_button = _ImageButton(
            button_img,
            center=(SCREEN_WIDTH // 2 - spacing, button_y),
            on_click=self.on_summon_again_click,
            scale=1.2,
            use_mask=True,
            text="SUMMON AGAIN",
            font=button_font
        )
        
        self.return_lobby_button = _ImageButton(
            button_img,
            center=(SCREEN_WIDTH // 2 + spacing, button_y),
            on_click=self.on_return_lobby_click,
            scale=1.2,
            use_mask=True,
            text="RETURN TO LOBBY",
            font=button_font
        )
    
    def _perform_summon(self, count):
        """ทำการสุ่มฮีโร่"""
        cost = SUMMON_COSTS[f'celestial_x{count}']
        
        # ตรวจสอบเหรียญ
        if self.player_data['coins'] < cost:
            print("Not enough coins!")
            return
        
        # หักเหรียญ
        player.spend_coins(self.player_data, cost)
        
        # เพิ่ม animation เหรียญที่ถูกหัก
        self._add_coin_animation(cost)
        
        # สุ่มฮีโร่
        self.summoned_heroes = []
        self.new_heroes = []
        
        for i in range(count):
            # สุ่ม rarity (มี EXTREME)
            roll = random.random()
            cumulative = 0.0
            selected_rarity = 'rare'
            
            for rarity in ['extreme', 'legendary', 'epic', 'rare']:
                cumulative += self.celestial_rates[rarity]
                if roll <= cumulative:
                    selected_rarity = rarity
                    break
            
            # สุ่มฮีโร่จาก pool
            hero_pool = self.hero_pools[selected_rarity]
            if hero_pool:
                hero = random.choice(hero_pool)
                self.summoned_heroes.append(hero)
                
                # ตรวจสอบว่าเป็นฮีโร่ใหม่หรือไม่
                if hero.id not in self.player_data['owned_heroes']:
                    self.new_heroes.append(hero)
                    player.add_hero(self.player_data, hero.id)
        
        # บันทึกข้อมูล
        self.game.save_game()
        
        # เตรียมการ์ด
        self._setup_cards()
        
        # เปลี่ยนสถานะ
        self.current_state = self.STATE_REVEALING
        self.current_new_hero_index = 0
    
    def _setup_cards(self):
        """เตรียมตำแหน่งการ์ดและโหลดรูปการ์ดหน้า/หลัง"""
        card_count = len(self.summoned_heroes)
        self.revealed_cards = [False] * card_count
        self.card_positions = []
        self.card_rects = []
        self.card_front_images = []
        self.card_back_images = []
        self.card_animations = [CardFlipAnimation(duration=0.3) for _ in range(card_count)]
        
        # โหลดรูปการ์ดหน้าและหลังสำหรับแต่ละฮีโร่
        for hero in self.summoned_heroes:
            # โหลดการ์ดหน้า
            try:
                card_front = assets.load_image(hero.card_front_path, (100, 140))
                self.card_front_images.append(card_front)
            except Exception as e:
                print(f"Warning: Could not load card front for {hero.name}: {e}")
                fallback = pygame.Surface((100, 140))
                fallback.fill((100, 100, 200))
                self.card_front_images.append(fallback)
            
            # โหลดการ์ดหลัง (แต่ละ rarity ต่างกัน)
            try:
                card_back = assets.load_image(hero.card_back_path, (100, 140))
                self.card_back_images.append(card_back)
            except Exception as e:
                print(f"Warning: Could not load card back for {hero.name}: {e}")
                fallback = pygame.Surface((100, 140))
                fallback.fill((139, 69, 19))
                self.card_back_images.append(fallback)
        
        # คำนวณตำแหน่งการ์ด
        card_width = 100
        card_height = 140
        
        if card_count == 1:
            # สุ่ม 1 ครั้ง - วางตรงกลาง
            x = (SCREEN_WIDTH - card_width) // 2
            y = (SCREEN_HEIGHT - card_height) // 2
            self.card_positions.append((x, y))
            self.card_rects.append(pygame.Rect(x, y, card_width, card_height))
        else:
            # สุ่ม 10 ครั้ง - grid 5x2
            cols = 5
            rows = 2
            spacing_x = 20
            spacing_y = 20
            
            total_width = cols * card_width + (cols - 1) * spacing_x
            total_height = rows * card_height + (rows - 1) * spacing_y
            
            start_x = (SCREEN_WIDTH - total_width) // 2
            start_y = (SCREEN_HEIGHT - total_height) // 2 - 50
            
            for i in range(card_count):
                row = i // cols
                col = i % cols
                x = start_x + col * (card_width + spacing_x)
                y = start_y + row * (card_height + spacing_y)
                
                self.card_positions.append((x, y))
                self.card_rects.append(pygame.Rect(x, y, card_width, card_height))
    
    def _add_coin_animation(self, cost):
        """เพิ่ม animation เหรียญที่ถูกหัก"""
        text = f"-{cost}"
        x = SCREEN_WIDTH // 2
        y = SCREEN_HEIGHT // 2
        alpha = 255
        timer = 2.0  # แสดง 2 วินาที
        self.coin_animations.append([text, x, y, alpha, timer])
    
    def on_summon_x1_click(self):
        """สุ่ม 1 ครั้ง"""
        self._perform_summon(1)
    
    def on_summon_x10_click(self):
        """สุ่ม 10 ครั้ง"""
        self._perform_summon(10)
    
    def on_back_click(self):
        """กลับไปหน้า lobby"""
        self.game.change_state('main_lobby')
    
    def on_question_click(self):
        """ไปหน้าแสดงข้อมูล Celestial Chest"""
        self.game.change_state('celestial_info')
    
    def on_summon_again_click(self):
        """สุ่มอีกครั้ง"""
        self.current_state = self.STATE_SELECTION
        self.summoned_heroes = []
        self.new_heroes = []
    
    def on_return_lobby_click(self):
        """กลับไปหน้า lobby"""
        self.game.change_state('main_lobby')
    
    def handle_event(self, event):
        """จัดการ event"""
        if self.current_state == self.STATE_SELECTION:
            if self.summon_x1_button:
                self.summon_x1_button.handle_event(event)
            if self.summon_x10_button:
                self.summon_x10_button.handle_event(event)
            if self.back_button:
                self.back_button.handle_event(event)
            if self.question_button:
                self.question_button.handle_event(event)
        
        elif self.current_state == self.STATE_REVEALING:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                
                # ตรวจสอบว่าคลิกที่การ์ดไหน
                clicked_card = False
                for i, rect in enumerate(self.card_rects):
                    if rect.collidepoint(mouse_pos) and not self.revealed_cards[i]:
                        self.revealed_cards[i] = True
                        self.card_animations[i].start()  # เริ่ม animation
                        clicked_card = True
                        break
                
                # ถ้าไม่ได้คลิกที่การ์ด = เปิดทั้งหมด
                if not clicked_card:
                    for i in range(len(self.revealed_cards)):
                        if not self.revealed_cards[i]:
                            self.revealed_cards[i] = True
                            self.card_animations[i].start()  # เริ่ม animation
        
        elif self.current_state == self.STATE_NEW_HERO:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # ไปฮีโร่ใหม่ตัวถัดไป
                self.current_new_hero_index += 1
                if self.current_new_hero_index >= len(self.new_heroes):
                    # แสดงฮีโร่ใหม่ครบแล้ว - ไปหน้าผลลัพธ์
                    self.current_state = self.STATE_RESULTS
                    self._create_result_buttons()
        
        elif self.current_state == self.STATE_RESULTS:
            if self.summon_again_button:
                self.summon_again_button.handle_event(event)
            if self.return_lobby_button:
                self.return_lobby_button.handle_event(event)
    
    def update(self, dt):
        """อัปเดตสถานะ"""
        # อัปเดต animation เหรียญ
        for anim in self.coin_animations[:]:
            anim[4] -= dt  # ลด timer
            anim[2] -= 50 * dt  # ลอยขึ้น
            anim[3] = max(0, anim[3] - 128 * dt)  # fade out
            
            if anim[4] <= 0:
                self.coin_animations.remove(anim)
        
        if self.current_state == self.STATE_SELECTION:
            if self.summon_x1_button:
                self.summon_x1_button.update(dt)
            if self.summon_x10_button:
                self.summon_x10_button.update(dt)
            if self.back_button:
                self.back_button.update(dt)
            if self.question_button:
                self.question_button.update(dt)
        
        elif self.current_state == self.STATE_REVEALING:
            # อัปเดต animation ของการ์ด
            all_animations_done = True
            for i, anim in enumerate(self.card_animations):
                if self.revealed_cards[i]:
                    anim.update(dt)
                    if anim.active:
                        all_animations_done = False
            
            # ถ้า animation เสร็จหมดและเปิดครบแล้ว
            if all_animations_done and all(self.revealed_cards):
                if self.new_heroes:
                    # มีฮีโร่ใหม่ - ไปหน้าแสดงฮีโร่ใหม่
                    self.current_state = self.STATE_NEW_HERO
                    self.current_new_hero_index = 0
                else:
                    # ไม่มีฮีโร่ใหม่ - ไปหน้าผลลัพธ์
                    self.current_state = self.STATE_RESULTS
                    self._create_result_buttons()
        
        elif self.current_state == self.STATE_RESULTS:
            if self.summon_again_button:
                self.summon_again_button.update(dt)
            if self.return_lobby_button:
                self.return_lobby_button.update(dt)
    
    def draw(self, screen):
        """วาดหน้าจอ"""
        # วาดพื้นหลัง
        if self.background:
            screen.blit(self.background, (0, 0))
        
        if self.current_state == self.STATE_SELECTION:
            self._draw_selection(screen)
        elif self.current_state == self.STATE_REVEALING:
            self._draw_revealing(screen)
        elif self.current_state == self.STATE_NEW_HERO:
            self._draw_new_hero(screen)
        elif self.current_state == self.STATE_RESULTS:
            self._draw_results(screen)
    
    def _draw_selection(self, screen):
        """วาดหน้าเลือกสุ่ม"""
        # หัวข้อ
        if self.font_title:
            title = self.font_title.render("CELESTIAL CHEST", True, (203, 108, 230))
            screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        
        # ปุ่ม
        if self.summon_x1_button:
            self.summon_x1_button.draw(screen)
            # แสดงราคาใต้ปุ่ม x1
            if self.font_normal:
                cost_text = f"{SUMMON_COSTS['celestial_x1']} coins"
                cost_surf = self.font_normal.render(cost_text, True, (255, 215, 0))
                cost_x = self.summon_x1_button.rect.centerx - cost_surf.get_width() // 2
                cost_y = self.summon_x1_button.rect.bottom + 10
                screen.blit(cost_surf, (cost_x, cost_y))
        
        if self.summon_x10_button:
            self.summon_x10_button.draw(screen)
            # แสดงราคาใต้ปุ่ม x10
            if self.font_normal:
                cost_text = f"{SUMMON_COSTS['celestial_x10']} coins"
                cost_surf = self.font_normal.render(cost_text, True, (255, 215, 0))
                cost_x = self.summon_x10_button.rect.centerx - cost_surf.get_width() // 2
                cost_y = self.summon_x10_button.rect.bottom + 10
                screen.blit(cost_surf, (cost_x, cost_y))
        
        if self.back_button:
            self.back_button.draw(screen)
        
        # วาด animation เหรียญที่ถูกหัก
        for anim in self.coin_animations:
            text, x, y, alpha, timer = anim
            if self.font_large:
                coin_surf = self.font_large.render(text, True, (255, 100, 100))
                coin_surf.set_alpha(int(alpha))
                screen.blit(coin_surf, (x - coin_surf.get_width() // 2, y))
        if self.question_button:
            self.question_button.draw(screen)
    
    def _draw_revealing(self, screen):
        """วาดหน้าเปิดการ์ดพร้อม flip animation"""
        # วาดการ์ด
        for i, pos in enumerate(self.card_positions):
            if self.revealed_cards[i]:
                anim = self.card_animations[i]
                
                # คำนวณ scale จาก animation
                scale_x = anim.get_scale_x()
                
                # เลือกรูปที่จะแสดง (หลังหรือหน้า)
                if anim.is_back_visible():
                    # แสดงการ์ดหลัง (ของฮีโร่นั้นๆ)
                    card_img = self.card_back_images[i]
                else:
                    # แสดงการ์ดหน้า
                    card_img = self.card_front_images[i]
                
                # ปรับขนาดตาม scale_x
                scaled_width = int(100 * scale_x)
                if scaled_width > 0:
                    scaled_card = pygame.transform.scale(card_img, (scaled_width, 140))
                    # วาดตรงกลางตำแหน่งเดิม
                    offset_x = (100 - scaled_width) // 2
                    screen.blit(scaled_card, (pos[0] + offset_x, pos[1]))
            else:
                # แสดงการ์ดหลัง (ยังไม่เปิด - ของฮีโร่นั้นๆ)
                screen.blit(self.card_back_images[i], pos)
        
        # แสดงข้อความ "TAP TO REVEAL!" ถ้ายังไม่เปิดครบ
        if not all(self.revealed_cards):
            if self.font_normal:
                text = self.font_normal.render("TAP TO REVEAL!", True, (255, 255, 255))
                screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT - 100))
    
    def _draw_new_hero(self, screen):
        """วาดหน้าแสดงฮีโร่ใหม่"""
        if self.current_new_hero_index < len(self.new_heroes):
            hero = self.new_heroes[self.current_new_hero_index]
            
            # หัวข้อ
            if self.font_title:
                title = self.font_title.render("NEW HERO UNLOCKED!", True, (255, 255, 255))
                screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
            
            # รูปฮีโร่ (รักษาอัตราส่วนเดิม)
            try:
                hero_img_original = assets.load_image(hero.portrait_path)
                
                # คำนวณขนาดใหม่โดยรักษาอัตราส่วน (ความสูงไม่เกิน 400px)
                original_width = hero_img_original.get_width()
                original_height = hero_img_original.get_height()
                
                max_height = 400
                scale = max_height / original_height
                new_width = int(original_width * scale)
                new_height = int(original_height * scale)
                
                hero_img = pygame.transform.smoothscale(hero_img_original, (new_width, new_height))
                
                # วางตรงกลาง
                x = SCREEN_WIDTH // 2 - new_width // 2
                y = SCREEN_HEIGHT // 2 - new_height // 2 + 20
                screen.blit(hero_img, (x, y))
            except Exception as e:
                print(f"Warning: Could not load hero portrait: {e}")
                pygame.draw.rect(screen, (100, 100, 200), 
                               (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 150, 300, 300))
    
    def _draw_results(self, screen):
        """วาดหน้าผลลัพธ์"""
        # วาดการ์ดทั้งหมด (เปิดหมดแล้ว)
        for i, pos in enumerate(self.card_positions):
            card_front = self.card_front_images[i]
            screen.blit(card_front, pos)
        
        # ปุ่ม
        if self.summon_again_button:
            self.summon_again_button.draw(screen)
        if self.return_lobby_button:
            self.return_lobby_button.draw(screen)
    
    def exit(self):
        """เรียกเมื่อออกจากหน้านี้"""
        pass
