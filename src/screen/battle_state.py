"""Battle State - ระบบต่อสู้ระหว่าง Player 1 และ Player 2"""
import pygame
import random
from src.core.game_state import GameState
from src.utils import assets
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.data.hero_data import get_hero
from src.utils import player
from src.ui.animation import CardFlipAnimation


class BattleState(GameState):
    """หน้า Battle - ผู้เล่น 2 คนเลือกการ์ดต่อสู้กัน"""
    
    def __init__(self, game):
        super().__init__(game)
        self.background = None
        self.font_title = None
        self.font_normal = None
        self.font_large = None
        self.font_small = None
        
        # ข้อมูลผู้เล่น
        self.player1_data = None
        self.player2_data = None
        
        # สถานะเกม
        self.phase = "BET"  # BET, P1_SELECT, P1_CONFIRM, P1_WAIT, P2_SELECT, P2_CONFIRM, P2_WAIT, ROUND_COMPARE, ROUND_RESULT, FINAL_RESULT
        self.bet_amount = 0
        self.bet_input = ""
        
        # ปุ่มยืนยัน
        self.confirm_button_rect = None
        self.back_button_rect = None
        self.clear_button_rect = None
        self.button_img = None
        self.button_img_hover = None
        
        # การ์ดที่เลือก
        self.p1_hand = []  # 5 ใบที่สุ่มมา
        self.p2_hand = []
        self.p1_card_order = []  # ลำดับการ์ดที่เลือก [hero_id1, hero_id2, ...]
        self.p2_card_order = []
        
        # ระบบต่อสู้ทีละรอบ
        self.current_round = 0  # รอบปัจจุบัน (0-4)
        self.p1_wins = 0  # จำนวนรอบที่ชนะ
        self.p2_wins = 0
        self.round_results = []  # ผลแต่ละรอบ
        
        # Animation
        self.compare_timer = 0
        self.compare_duration = 3.0
        self.result_timer = 0
        self.winner = None
        self.compare_finished = False
        self.blink_timer = 0
        
        # UI Elements
        self.card_rects = []
        self.selected_card_index = -1
        
        # Animation
        self.card_animations = []
        self.revealed_cards = []
        self.card_back_images = []
        self.card_front_images = []
        
    def enter(self):
        # โหลดพื้นหลัง
        try:
            self.background = assets.load_image('assets/backgrounds/arena.png').convert()
        except:
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((40, 20, 20))
        
        # โหลดฟอนต์
        try:
            self.font_title = assets.load_font('assets/fonts/Monocraft.ttf', 32)
            self.font_normal = assets.load_font('assets/fonts/Monocraft.ttf', 20)
            self.font_large = assets.load_font('assets/fonts/Monocraft.ttf', 48)
            self.font_small = assets.load_font('assets/fonts/Monocraft.ttf', 15)
        except:
            self.font_title = pygame.font.Font(None, 32)
            self.font_normal = pygame.font.Font(None, 20)
            self.font_large = pygame.font.Font(None, 48)
            self.font_small = pygame.font.Font(None, 15)
        
        # โหลดรูปปุ่ม
        try:
            self.button_img = assets.load_image('assets/ui/12.png').convert_alpha()
        except:
            self.button_img = pygame.Surface((220, 70), pygame.SRCALPHA)
            self.button_img.fill((60, 60, 90, 255))
        
        # โหลดข้อมูลผู้เล่นทั้ง 2 คน
        self.player1_data = player.load_player_data(1)
        self.player2_data = player.load_player_data(2)
        
        # เริ่มต้นเฟส BET
        self.phase = "BET"
        self.bet_amount = 0
        self.bet_input = ""
        
    def handle_event(self, event):
        if self.phase == "BET":
            self._handle_bet_input(event)
        elif self.phase == "P1_SELECT":
            # สร้างปุ่มถ้ายังไม่มี
            if not self.confirm_button_rect:
                self._create_confirm_button()
            # จัดการทั้งการเลือกการ์ดและปุ่ม
            self._handle_card_selection(event, 1)
            self._handle_confirm_button(event, 1)
        elif self.phase == "P2_SELECT":
            # สร้างปุ่มถ้ายังไม่มี
            if not self.confirm_button_rect:
                self._create_confirm_button()
            # จัดการทั้งการเลือกการ์ดและปุ่ม
            self._handle_card_selection(event, 2)
            self._handle_confirm_button(event, 2)
        elif self.phase == "ROUND_COMPARE":
            # ให้กด Enter เพื่อดูผลรอบนี้
            if self.compare_finished and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self._calculate_round_result()
        elif self.phase == "ROUND_RESULT":
            # กด Enter เพื่อไปรอบถัดไป
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self._next_round_or_finish()
        elif self.phase == "FINAL_RESULT":
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self._return_to_loading()
    
    def _handle_bet_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # ยืนยันจำนวนเงิน
                try:
                    amount = int(self.bet_input)
                    min_coins = min(self.player1_data['coins'], self.player2_data['coins'])
                    if amount > 0 and amount <= min_coins:
                        self.bet_amount = amount
                        self._start_player1_turn()
                    else:
                        print(f"จำนวนเงินไม่ถูกต้อง (ต้อง 1-{min_coins})")
                except ValueError:
                    print("กรุณากรอกตัวเลข")
            elif event.key == pygame.K_BACKSPACE:
                self.bet_input = self.bet_input[:-1]
            elif event.unicode.isdigit() and len(self.bet_input) < 6:
                self.bet_input += event.unicode
    
    def _start_player1_turn(self):
        """เริ่มเทิร์นผู้เล่น 1 - สุ่มการ์ด 5 ใบ"""
        self.phase = "P1_SELECT"
        owned_heroes = self.player1_data['owned_heroes']
        if len(owned_heroes) >= 5:
            self.p1_hand = random.sample(owned_heroes, 5)
        else:
            self.p1_hand = owned_heroes.copy()
        self.p1_card_order = []  # รีเซ็ตลำดับ
        self._setup_card_rects()
        self._setup_card_animations(self.p1_hand)
    
    def _start_player2_turn(self):
        """เริ่มเทิร์นผู้เล่น 2 - สุ่มการ์ด 5 ใบ"""
        self.phase = "P2_SELECT"
        owned_heroes = self.player2_data['owned_heroes']
        if len(owned_heroes) >= 5:
            self.p2_hand = random.sample(owned_heroes, 5)
        else:
            self.p2_hand = owned_heroes.copy()
        self.p2_card_order = []  # รีเซ็ตลำดับ
        self._setup_card_rects()
        self._setup_card_animations(self.p2_hand)
    
    def _setup_card_rects(self):
        """สร้าง rect สำหรับการ์ด 5 ใบ"""
        self.card_rects = []
        card_width = 120
        card_height = 160
        spacing = 20
        total_width = card_width * 5 + spacing * 4
        start_x = (SCREEN_WIDTH - total_width) // 2
        y = SCREEN_HEIGHT - card_height - 30
        
        for i in range(5):
            x = start_x + i * (card_width + spacing)
            self.card_rects.append(pygame.Rect(x, y, card_width, card_height))
    
    def _setup_card_animations(self, hand):
        """เตรียม animation สำหรับการ์ด"""
        self.revealed_cards = [False] * len(hand)
        self.card_animations = [CardFlipAnimation(duration=0.3) for _ in range(len(hand))]
        self.card_back_images = []
        self.card_front_images = []
        
        # โหลดรูปการ์ดหน้าและหลัง
        for hero_id in hand:
            hero = get_hero(hero_id)
            if hero:
                # โหลดการ์ดหน้า
                try:
                    card_front = assets.load_image(hero.card_front_path, (120, 160))
                    self.card_front_images.append(card_front)
                except:
                    fallback = pygame.Surface((120, 160))
                    fallback.fill((100, 100, 200))
                    self.card_front_images.append(fallback)
                
                # โหลดการ์ดหลัง
                try:
                    card_back = assets.load_image(hero.card_back_path, (120, 160))
                    self.card_back_images.append(card_back)
                except:
                    fallback = pygame.Surface((120, 160))
                    fallback.fill((139, 69, 19))
                    self.card_back_images.append(fallback)
        
        # เริ่ม animation ทีละใบ (delay 0.2 วินาทีต่อใบ)
        for i, anim in enumerate(self.card_animations):
            anim.start(delay=i * 0.2)
    
    def _handle_card_selection(self, event, player_num):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # ตรวจสอบว่า animation เสร็จหมดแล้วหรือยัง
            all_revealed = all(self.revealed_cards)
            if not all_revealed:
                return
            
            hand = self.p1_hand if player_num == 1 else self.p2_hand
            card_order = self.p1_card_order if player_num == 1 else self.p2_card_order
            
            for i, rect in enumerate(self.card_rects):
                if rect.collidepoint(event.pos):
                    hero_id = hand[i]
                    
                    # ถ้าการ์ดนี้ถูกเลือกแล้ว → ลบออก
                    if hero_id in card_order:
                        card_order.remove(hero_id)
                    # ถ้ายังไม่ได้เลือก และยังไม่ครบ 5 → เพิ่มเข้าลำดับ
                    elif len(card_order) < 5:
                        card_order.append(hero_id)
                    
                    # อัปเดตกลับ
                    if player_num == 1:
                        self.p1_card_order = card_order
                    else:
                        self.p2_card_order = card_order
                    
                    break
    
    def _create_confirm_button(self):
        """สร้างปุ่มยืนยัน, CLEAR และย้อนกลับ"""
        # ปรับขนาดปุ่ม
        button_scale = 1.2
        button_width = int(self.button_img.get_width() * button_scale)
        button_height = int(self.button_img.get_height() * button_scale)
        spacing = 20
        
        # คำนวณตำแหน่งให้อยู่ตรงกลางหน้าจอ (แนวนอนและแนวตั้ง)
        total_width = button_width * 3 + spacing * 2
        start_x = (SCREEN_WIDTH - total_width) // 2
        button_y = SCREEN_HEIGHT // 2 - button_height // 2
        
        # ปุ่มยืนยัน (ซ้าย)
        self.confirm_button_rect = pygame.Rect(
            start_x,
            button_y,
            button_width,
            button_height
        )
        
        # ปุ่ม CLEAR (กลาง)
        self.clear_button_rect = pygame.Rect(
            start_x + button_width + spacing,
            button_y,
            button_width,
            button_height
        )
        
        # ปุ่มย้อนกลับ (ขวา)
        self.back_button_rect = pygame.Rect(
            start_x + (button_width + spacing) * 2,
            button_y,
            button_width,
            button_height
        )
    
    def _handle_confirm_button(self, event, player_num):
        """จัดการปุ่มยืนยัน, CLEAR และย้อนกลับ"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            card_order = self.p1_card_order if player_num == 1 else self.p2_card_order
            
            # ปุ่มยืนยัน (ต้องเลือกครบ 5 ใบ)
            if self.confirm_button_rect and self.confirm_button_rect.collidepoint(event.pos):
                if len(card_order) == 5:
                    if player_num == 1:
                        self.phase = "P1_WAIT"
                        self._start_player2_turn()
                    else:
                        self.phase = "P2_WAIT"
                        self._start_rounds()
            
            # ปุ่ม CLEAR
            elif self.clear_button_rect and self.clear_button_rect.collidepoint(event.pos):
                if player_num == 1:
                    self.p1_card_order = []
                else:
                    self.p2_card_order = []
            
            # ปุ่มย้อนกลับ (กลับไปหน้า BET)
            elif self.back_button_rect and self.back_button_rect.collidepoint(event.pos):
                self.phase = "BET"
                self.p1_card_order = []
                self.p2_card_order = []
                self.bet_input = ""
    
    def _start_rounds(self):
        """เริ่มการต่อสู้ทีละรอบ"""
        self.current_round = 0
        self.p1_wins = 0
        self.p2_wins = 0
        self.round_results = []
        self._start_round_compare()
    
    def _start_round_compare(self):
        """เริ่มเปรียบเทียบการ์ดในรอบปัจจุบัน"""
        self.phase = "ROUND_COMPARE"
        self.compare_timer = 0
        self.compare_finished = False
        self.blink_timer = 0
    
    def _calculate_round_result(self):
        """คำนวณผลรอบปัจจุบัน"""
        hero1_id = self.p1_card_order[self.current_round]
        hero2_id = self.p2_card_order[self.current_round]
        
        hero1 = get_hero(hero1_id)
        hero2 = get_hero(hero2_id)
        
        power1 = hero1.power if hero1 else 0
        power2 = hero2.power if hero2 else 0
        
        # บันทึกผลรอบนี้
        if power1 > power2:
            round_winner = 1
            self.p1_wins += 1
        elif power2 > power1:
            round_winner = 2
            self.p2_wins += 1
        else:
            round_winner = 0  # เสมอ
        
        self.round_results.append({
            'round': self.current_round + 1,
            'hero1': hero1,
            'hero2': hero2,
            'power1': power1,
            'power2': power2,
            'winner': round_winner
        })
        
        self.phase = "ROUND_RESULT"
        self.result_timer = 0
        self.blink_timer = 0
    
    def _next_round_or_finish(self):
        """ไปรอบถัดไปหรือจบเกม"""
        # ตรวจสอบว่ามีคนชนะ 3 รอบแล้วหรือยัง
        if self.p1_wins >= 3 or self.p2_wins >= 3:
            self._calculate_final_result()
            return
        
        # ตรวจสอบว่าครบ 5 รอบหรือยัง
        self.current_round += 1
        if self.current_round >= 5:
            self._calculate_final_result()
        else:
            self._start_round_compare()
    
    def _calculate_final_result(self):
        """คำนวณผลสุดท้าย"""
        # คำนวณเงินที่จะได้/เสีย โดยไม่ให้ติดลบ
        actual_bet = min(self.bet_amount, self.player1_data['coins'], self.player2_data['coins'])
        
        if self.p1_wins > self.p2_wins:
            self.winner = 1
            self.player1_data['coins'] += actual_bet
            self.player2_data['coins'] -= actual_bet
            self.player1_data['rank'] += 1
        elif self.p2_wins > self.p1_wins:
            self.winner = 2
            self.player2_data['coins'] += actual_bet
            self.player1_data['coins'] -= actual_bet
            self.player2_data['rank'] += 1
        else:
            self.winner = 0  # เสมอ
        
        # อัปเดต bet_amount เป็นจำนวนจริงที่ใช้
        self.bet_amount = actual_bet
        
        # บันทึกข้อมูล
        player.save_player_data(self.player1_data, 1)
        player.save_player_data(self.player2_data, 2)
        
        self.phase = "FINAL_RESULT"
        self.result_timer = 0
        self.blink_timer = 0
    
    def _return_to_loading(self):
        """กลับไปหน้า loading"""
        self.game.change_state('loading')
    
    def update(self, dt):
        # อัปเดต animation การ์ด
        if self.phase in ["P1_SELECT", "P1_CONFIRM", "P2_SELECT", "P2_CONFIRM"]:
            for i, anim in enumerate(self.card_animations):
                anim.update(dt)
                # ถ้า animation เสร็จแล้ว ให้ถือว่าเปิดแล้ว
                if not anim.active and not self.revealed_cards[i]:
                    self.revealed_cards[i] = True
        
        if self.phase == "ROUND_COMPARE":
            self.compare_timer += dt
            if self.compare_timer >= self.compare_duration:
                self.compare_finished = True
            
            # อัปเดต blink timer
            if self.compare_finished:
                self.blink_timer += dt
        elif self.phase in ["ROUND_RESULT", "FINAL_RESULT"]:
            self.result_timer += dt
            self.blink_timer += dt
    
    def draw(self, screen: pygame.Surface):
        # พื้นหลัง
        screen.blit(self.background, (0, 0))
        
        if self.phase == "BET":
            self._draw_bet_phase(screen)
        elif self.phase in ["P1_SELECT", "P1_CONFIRM"]:
            self._draw_select_phase(screen, 1)
        elif self.phase == "P1_WAIT":
            self._draw_wait_phase(screen, 1)
        elif self.phase in ["P2_SELECT", "P2_CONFIRM"]:
            self._draw_select_phase(screen, 2)
        elif self.phase == "P2_WAIT":
            self._draw_wait_phase(screen, 2)
        elif self.phase == "ROUND_COMPARE":
            self._draw_round_compare_phase(screen)
        elif self.phase == "ROUND_RESULT":
            self._draw_round_result_phase(screen)
        elif self.phase == "FINAL_RESULT":
            self._draw_final_result_phase(screen)
    
    def _draw_bet_phase(self, screen):
        """วาดหน้ากรอกจำนวนเงิน"""
        # กรอบกลาง
        box = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100, 400, 200)
        pygame.draw.rect(screen, (50, 50, 50, 200), box)
        pygame.draw.rect(screen, (255, 255, 255), box, 3)
        
        # หัวข้อ
        title = self.font_title.render("ENTER BET AMOUNT", True, (255, 255, 255))
        screen.blit(title, (box.centerx - title.get_width() // 2, box.y + 20))
        
        # ช่องกรอก
        input_box = pygame.Rect(box.centerx - 150, box.centery - 20, 300, 50)
        pygame.draw.rect(screen, (30, 30, 30), input_box)
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)
        
        input_text = self.font_normal.render(self.bet_input, True, (255, 255, 255))
        screen.blit(input_text, (input_box.x + 10, input_box.y + 12))
        
        # คำแนะนำ
        min_coins = min(self.player1_data['coins'], self.player2_data['coins'])
        hint = self.font_normal.render(f"Max: {min_coins} coins", True, (200, 200, 200))
        screen.blit(hint, (box.centerx - hint.get_width() // 2, box.bottom - 40))
    
    def _draw_select_phase(self, screen, player_num):
        """วาดหน้าเลือกการ์ด"""
        # แสดงผู้เล่นที่กำลังเลือก
        title = self.font_title.render(f"PLAYER {player_num} - SELECT CARD", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
        
        # แสดงการ์ด 5 ใบพร้อม animation
        hand = self.p1_hand if player_num == 1 else self.p2_hand
        for i, (hero_id, rect) in enumerate(zip(hand, self.card_rects)):
            hero = get_hero(hero_id)
            if hero:
                anim = self.card_animations[i]
                
                # คำนวณ scale จาก animation
                scale_x = anim.get_scale_x()
                
                # เลือกรูปที่จะแสดง (หลังหรือหน้า)
                if anim.is_back_visible():
                    # แสดงการ์ดหลัง
                    card_img = self.card_back_images[i]
                else:
                    # แสดงการ์ดหน้า
                    card_img = self.card_front_images[i]
                
                # ปรับขนาดตาม scale_x
                scaled_width = int(rect.width * scale_x)
                if scaled_width > 0:
                    scaled_card = pygame.transform.scale(card_img, (scaled_width, rect.height))
                    # วาดตรงกลางตำแหน่งเดิม
                    offset_x = (rect.width - scaled_width) // 2
                    screen.blit(scaled_card, (rect.x + offset_x, rect.y))
                
                # แสดงเลขลำดับ (ถ้าถูกเลือก)
                if self.revealed_cards[i]:
                    card_order = self.p1_card_order if player_num == 1 else self.p2_card_order
                    if hero_id in card_order:
                        order_num = card_order.index(hero_id) + 1
                        # แสดงเลขลำดับ (สีขาว, ตัวเล็กลง)
                        order_text = self.font_normal.render(str(order_num), True, (255, 255, 255))
                        screen.blit(order_text, (rect.centerx - order_text.get_width() // 2, 
                                                rect.centery - order_text.get_height() // 2))
                    
                    # แสดงพลัง
                    power_text = self.font_normal.render(str(hero.power), True, (255, 255, 255))
                    screen.blit(power_text, (rect.centerx - power_text.get_width() // 2, rect.bottom + 5))
        
        # แสดงข้อความรอ animation
        if not all(self.revealed_cards):
            hint = self.font_normal.render("Revealing cards...", True, (200, 200, 200))
            screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 50))
        else:
            # แสดงปุ่ม CONFIRM, CLEAR, BACK
            self._draw_selection_buttons(screen, player_num)
    
    def _draw_selection_buttons(self, screen, player_num):
        """วาดปุ่ม CONFIRM, CLEAR, BACK"""
        mouse_pos = pygame.mouse.get_pos()
        card_order = self.p1_card_order if player_num == 1 else self.p2_card_order
        
        # ปุ่ม CONFIRM (เปิดใช้งานเมื่อเลือกครบ 5)
        if self.confirm_button_rect and self.button_img:
            is_hover = self.confirm_button_rect.collidepoint(mouse_pos)
            is_enabled = len(card_order) == 5
            button_scale = 1.2
            scaled_img = pygame.transform.scale(
                self.button_img,
                (int(self.button_img.get_width() * button_scale), 
                 int(self.button_img.get_height() * button_scale))
            )
            
            if not is_enabled:
                scaled_img = scaled_img.copy()
                scaled_img.fill((100, 100, 100, 255), special_flags=pygame.BLEND_RGBA_MULT)
            elif is_hover:
                scaled_img = scaled_img.copy()
                scaled_img.fill((230, 240, 245, 255), special_flags=pygame.BLEND_RGBA_MULT)
            
            screen.blit(scaled_img, self.confirm_button_rect)
            button_text = self.font_small.render("CONFIRM", True, (255, 255, 255))
            screen.blit(button_text, (
                self.confirm_button_rect.centerx - button_text.get_width() // 2,
                self.confirm_button_rect.centery - button_text.get_height() // 2
            ))
        
        # ปุ่ม CLEAR
        if self.clear_button_rect and self.button_img:
            is_hover = self.clear_button_rect.collidepoint(mouse_pos)
            button_scale = 1.2
            scaled_img = pygame.transform.scale(
                self.button_img,
                (int(self.button_img.get_width() * button_scale), 
                 int(self.button_img.get_height() * button_scale))
            )
            
            if is_hover:
                scaled_img = scaled_img.copy()
                scaled_img.fill((230, 240, 245, 255), special_flags=pygame.BLEND_RGBA_MULT)
            
            screen.blit(scaled_img, self.clear_button_rect)
            button_text = self.font_small.render("CLEAR", True, (255, 255, 255))
            screen.blit(button_text, (
                self.clear_button_rect.centerx - button_text.get_width() // 2,
                self.clear_button_rect.centery - button_text.get_height() // 2
            ))
        
        # ปุ่ม BACK
        if self.back_button_rect and self.button_img:
            is_hover = self.back_button_rect.collidepoint(mouse_pos)
            button_scale = 1.2
            scaled_img = pygame.transform.scale(
                self.button_img,
                (int(self.button_img.get_width() * button_scale), 
                 int(self.button_img.get_height() * button_scale))
            )
            
            if is_hover:
                scaled_img = scaled_img.copy()
                scaled_img.fill((230, 240, 245, 255), special_flags=pygame.BLEND_RGBA_MULT)
            
            screen.blit(scaled_img, self.back_button_rect)
            button_text = self.font_small.render("BACK", True, (255, 255, 255))
            screen.blit(button_text, (
                self.back_button_rect.centerx - button_text.get_width() // 2,
                self.back_button_rect.centery - button_text.get_height() // 2
            ))
        
        # แสดงจำนวนที่เลือก
        status_text = f"Selected: {len(card_order)}/5"
        status_surf = self.font_normal.render(status_text, True, (255, 255, 255))
        screen.blit(status_surf, (SCREEN_WIDTH // 2 - status_surf.get_width() // 2, 80))
    
    def _draw_confirm_phase(self, screen, player_num):
        """วาดหน้ายืนยันการเลือก"""
        # แสดงผู้เล่น
        title = self.font_title.render(f"PLAYER {player_num} - CONFIRM?", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
        
        # แสดงการ์ดที่เลือกตรงกลาง
        selected_card = self.p1_selected_card if player_num == 1 else self.p2_selected_card
        hero = get_hero(selected_card)
        
        if hero:
            card_width = 200
            card_height = 280
            card_x = SCREEN_WIDTH // 2 - card_width // 2
            card_y = SCREEN_HEIGHT // 2 - card_height // 2 - 80
            
            try:
                card_img = hero.get_card_front()
                card_img = pygame.transform.scale(card_img, (card_width, card_height))
                screen.blit(card_img, (card_x, card_y))
            except:
                pygame.draw.rect(screen, (100, 100, 100), (card_x, card_y, card_width, card_height))
            
            # แสดงพลัง
            power_text = self.font_large.render(f"Power: {hero.power}", True, (255, 255, 255))
            screen.blit(power_text, (SCREEN_WIDTH // 2 - power_text.get_width() // 2, card_y + card_height + 20))
        
        # วาดปุ่มด้วย frame
        mouse_pos = pygame.mouse.get_pos()
        
        # ปุ่มยืนยัน (ซ้าย)
        if self.confirm_button_rect and self.button_img:
            is_hover = self.confirm_button_rect.collidepoint(mouse_pos)
            button_scale = 1.2
            scaled_img = pygame.transform.scale(
                self.button_img,
                (int(self.button_img.get_width() * button_scale), 
                 int(self.button_img.get_height() * button_scale))
            )
            
            # ใช้ color effect ถ้า hover
            if is_hover:
                scaled_img = scaled_img.copy()
                scaled_img.fill((230, 240, 245, 255), special_flags=pygame.BLEND_RGBA_MULT)
            
            screen.blit(scaled_img, self.confirm_button_rect)
            
            button_text = self.font_small.render("CONFIRM", True, (255, 255, 255))
            screen.blit(button_text, (
                self.confirm_button_rect.centerx - button_text.get_width() // 2,
                self.confirm_button_rect.centery - button_text.get_height() // 2
            ))
        
        # ปุ่มย้อนกลับ (ขวา)
        if self.back_button_rect and self.button_img:
            is_hover = self.back_button_rect.collidepoint(mouse_pos)
            button_scale = 1.2
            scaled_img = pygame.transform.scale(
                self.button_img,
                (int(self.button_img.get_width() * button_scale), 
                 int(self.button_img.get_height() * button_scale))
            )
            
            # ใช้ color effect ถ้า hover
            if is_hover:
                scaled_img = scaled_img.copy()
                scaled_img.fill((230, 240, 245, 255), special_flags=pygame.BLEND_RGBA_MULT)
            
            screen.blit(scaled_img, self.back_button_rect)
            
            button_text = self.font_small.render("BACK", True, (255, 255, 255))
            screen.blit(button_text, (
                self.back_button_rect.centerx - button_text.get_width() // 2,
                self.back_button_rect.centery - button_text.get_height() // 2
            ))
    
    def _draw_wait_phase(self, screen, player_num):
        """วาดหน้ารอ - แสดงการ์ดที่เลือกไว้"""
        # แสดงข้อความรอ
        title = self.font_title.render(f"PLAYER {player_num} READY!", True, (255, 255, 255))
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 30))
        
        # แสดงการ์ดที่เลือกตรงกลาง
        selected_card = self.p1_selected_card if player_num == 1 else self.p2_selected_card
        hero = get_hero(selected_card)
        
        if hero:
            card_width = 200
            card_height = 280
            card_x = SCREEN_WIDTH // 2 - card_width // 2
            card_y = SCREEN_HEIGHT // 2 - card_height // 2
            
            try:
                card_img = hero.get_card_front()
                card_img = pygame.transform.scale(card_img, (card_width, card_height))
                screen.blit(card_img, (card_x, card_y))
            except:
                pygame.draw.rect(screen, (100, 100, 100), (card_x, card_y, card_width, card_height))
            
            # แสดงพลัง
            power_text = self.font_large.render(f"Power: {hero.power}", True, (255, 255, 255))
            screen.blit(power_text, (SCREEN_WIDTH // 2 - power_text.get_width() // 2, card_y + card_height + 20))
        
        # ข้อความรอ
        wait_text = self.font_normal.render("Waiting for other player...", True, (200, 200, 200))
        screen.blit(wait_text, (SCREEN_WIDTH // 2 - wait_text.get_width() // 2, SCREEN_HEIGHT - 50))
    
    def _draw_compare_phase(self, screen):
        """วาดหน้าเปรียบเทียบการ์ด"""
        # แสดงการ์ดทั้ง 2 ใบ
        hero1 = get_hero(self.p1_selected_card)
        hero2 = get_hero(self.p2_selected_card)
        
        card_width = 150
        card_height = 200
        
        # การ์ด Player 1 (ซ้าย)
        p1_rect = pygame.Rect(SCREEN_WIDTH // 2 - card_width - 50, SCREEN_HEIGHT // 2 - card_height // 2, card_width, card_height)
        # การ์ด Player 2 (ขวา)
        p2_rect = pygame.Rect(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - card_height // 2, card_width, card_height)
        
        # วาดการ์ด
        for hero, rect, player_num in [(hero1, p1_rect, 1), (hero2, p2_rect, 2)]:
            if hero:
                try:
                    card_img = hero.get_card_front()
                    card_img = pygame.transform.scale(card_img, (rect.width, rect.height))
                    screen.blit(card_img, rect)
                except:
                    pygame.draw.rect(screen, (100, 100, 100), rect)
                
                # ชื่อผู้เล่น
                player_text = self.font_normal.render(f"Player {player_num}", True, (255, 255, 255))
                screen.blit(player_text, (rect.centerx - player_text.get_width() // 2, rect.y - 30))
        
        # Animation เปรียบเทียบพลัง
        progress = min(self.compare_timer / self.compare_duration, 1.0)
        
        if progress < 0.5:
            # ระยะที่ 1: แสดงพลังค่อยๆขึ้น
            anim_progress = progress * 2
            power1 = int(hero1.power * anim_progress) if hero1 else 0
            power2 = int(hero2.power * anim_progress) if hero2 else 0
            
            # แสดงตัวเลขพลัง
            p1_text = self.font_large.render(str(power1), True, (255, 255, 255))
            p2_text = self.font_large.render(str(power2), True, (255, 255, 255))
            screen.blit(p1_text, (p1_rect.centerx - p1_text.get_width() // 2, p1_rect.bottom + 20))
            screen.blit(p2_text, (p2_rect.centerx - p2_text.get_width() // 2, p2_rect.bottom + 20))
        else:
            # ระยะที่ 2: แสดงผลเต็มและเน้นผู้ชนะ
            power1 = hero1.power if hero1 else 0
            power2 = hero2.power if hero2 else 0
            power_diff = abs(power1 - power2)
            
            # กำหนดสีและขนาด
            if power1 > power2:
                color1, scale1 = (255, 255, 0), 1.2
                color2, scale2 = (255, 255, 255), 1.0
                diff1, diff2 = power_diff, 0
            elif power2 > power1:
                color1, scale1 = (255, 255, 255), 1.0
                color2, scale2 = (255, 255, 0), 1.2
                diff1, diff2 = 0, power_diff
            else:
                color1, scale1 = (255, 255, 255), 1.0
                color2, scale2 = (255, 255, 255), 1.0
                diff1, diff2 = 0, 0
            
            # วาดตัวเลขพลัง
            font_size1 = int(48 * scale1)
            font_size2 = int(48 * scale2)
            try:
                font1 = assets.load_font('assets/fonts/Monocraft.ttf', font_size1)
                font2 = assets.load_font('assets/fonts/Monocraft.ttf', font_size2)
                font_diff = assets.load_font('assets/fonts/Monocraft.ttf', 24)
            except:
                font1 = pygame.font.Font(None, font_size1)
                font2 = pygame.font.Font(None, font_size2)
                font_diff = pygame.font.Font(None, 24)
            
            # แสดงพลัง
            p1_text = font1.render(str(power1), True, color1)
            p2_text = font2.render(str(power2), True, color2)
            screen.blit(p1_text, (p1_rect.centerx - p1_text.get_width() // 2, p1_rect.bottom + 20))
            screen.blit(p2_text, (p2_rect.centerx - p2_text.get_width() // 2, p2_rect.bottom + 20))
            
            # แสดงผลต่าง (ใต้ค่าพลัง - ขยับลงมาหน่อย)
            diff1_text = font_diff.render(f"+{diff1}" if diff1 > 0 else "0", True, color1)
            diff2_text = font_diff.render(f"+{diff2}" if diff2 > 0 else "0", True, color2)
            screen.blit(diff1_text, (p1_rect.centerx - diff1_text.get_width() // 2, p1_rect.bottom + 85))
            screen.blit(diff2_text, (p2_rect.centerx - diff2_text.get_width() // 2, p2_rect.bottom + 85))
        
        # แสดงข้อความกด Enter (กระพริบ) หลัง animation เสร็จ
        if self.compare_finished:
            # กระพริบทุก 0.5 วินาที
            if int(self.blink_timer * 2) % 2 == 0:
                hint = self.font_normal.render("Press ENTER to continue", True, (200, 200, 200))
                screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 50))
    
    def _draw_result_phase(self, screen):
        """วาดหน้าผลลัพธ์"""
        # กรอบผลลัพธ์
        box = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 150, 500, 300)
        pygame.draw.rect(screen, (30, 30, 30, 220), box)
        pygame.draw.rect(screen, (255, 255, 255), box, 3)
        
        # ผลการแข่งขัน
        if self.winner == 1:
            result_text = "PLAYER 1 WINS!"
            color = (255, 215, 0)
        elif self.winner == 2:
            result_text = "PLAYER 2 WINS!"
            color = (255, 215, 0)
        else:
            result_text = "DRAW!"
            color = (200, 200, 200)
        
        result = self.font_large.render(result_text, True, color)
        screen.blit(result, (box.centerx - result.get_width() // 2, box.y + 40))
        
        # แสดง Scoreboard
        score_y = box.y + 120
        
        # Player 1
        p1_score = self.font_normal.render(f"Player 1 Score: {self.player1_data['rank']}", True, (255, 255, 255))
        screen.blit(p1_score, (box.centerx - p1_score.get_width() // 2, score_y))
        
        # Player 2
        p2_score = self.font_normal.render(f"Player 2 Score: {self.player2_data['rank']}", True, (255, 255, 255))
        screen.blit(p2_score, (box.centerx - p2_score.get_width() // 2, score_y + 30))
        
        # เงินที่ได้/เสีย
        money_y = score_y + 80
        if self.winner == 1:
            p1_money = self.font_normal.render(f"Player 1: +{self.bet_amount} coins", True, (0, 255, 0))
            p2_money = self.font_normal.render(f"Player 2: -{self.bet_amount} coins", True, (255, 0, 0))
        elif self.winner == 2:
            p1_money = self.font_normal.render(f"Player 1: -{self.bet_amount} coins", True, (255, 0, 0))
            p2_money = self.font_normal.render(f"Player 2: +{self.bet_amount} coins", True, (0, 255, 0))
        else:
            p1_money = self.font_normal.render(f"Player 1: 0 coins", True, (200, 200, 200))
            p2_money = self.font_normal.render(f"Player 2: 0 coins", True, (200, 200, 200))
        
        screen.blit(p1_money, (box.centerx - p1_money.get_width() // 2, money_y))
        screen.blit(p2_money, (box.centerx - p2_money.get_width() // 2, money_y + 30))
        
        # คำแนะนำ (กระพริบ)
        if int(self.blink_timer * 2) % 2 == 0:
            hint = self.font_normal.render("Press ENTER to continue", True, (200, 200, 200))
            screen.blit(hint, (box.centerx - hint.get_width() // 2, box.bottom - 40))
    
    def _draw_round_compare_phase(self, screen):
        """วาดหน้าเปรียบเทียบการ์ดในรอบปัจจุบัน"""
        # แสดงรอบปัจจุบัน
        round_text = f"ROUND {self.current_round + 1}/5"
        round_surf = self.font_title.render(round_text, True, (255, 255, 255))
        screen.blit(round_surf, (SCREEN_WIDTH // 2 - round_surf.get_width() // 2, 30))
        
        # แสดงคะแนน
        score_text = f"P1: {self.p1_wins}  -  P2: {self.p2_wins}"
        score_surf = self.font_normal.render(score_text, True, (255, 255, 255))
        screen.blit(score_surf, (SCREEN_WIDTH // 2 - score_surf.get_width() // 2, 80))
        
        # แสดงการ์ดทั้ง 2 ใบ
        hero1_id = self.p1_card_order[self.current_round]
        hero2_id = self.p2_card_order[self.current_round]
        hero1 = get_hero(hero1_id)
        hero2 = get_hero(hero2_id)
        
        card_width = 150
        card_height = 200
        
        p1_rect = pygame.Rect(SCREEN_WIDTH // 2 - card_width - 50, SCREEN_HEIGHT // 2 - card_height // 2, card_width, card_height)
        p2_rect = pygame.Rect(SCREEN_WIDTH // 2 + 50, SCREEN_HEIGHT // 2 - card_height // 2, card_width, card_height)
        
        # วาดการ์ด
        for hero, rect, player_num in [(hero1, p1_rect, 1), (hero2, p2_rect, 2)]:
            if hero:
                try:
                    card_img = hero.get_card_front()
                    card_img = pygame.transform.scale(card_img, (rect.width, rect.height))
                    screen.blit(card_img, rect)
                except:
                    pygame.draw.rect(screen, (100, 100, 100), rect)
                
                player_text = self.font_normal.render(f"Player {player_num}", True, (255, 255, 255))
                screen.blit(player_text, (rect.centerx - player_text.get_width() // 2, rect.y - 30))
        
        # Animation เปรียบเทียบพลัง
        progress = min(self.compare_timer / self.compare_duration, 1.0)
        
        if progress < 0.5:
            anim_progress = progress * 2
            power1 = int(hero1.power * anim_progress) if hero1 else 0
            power2 = int(hero2.power * anim_progress) if hero2 else 0
            
            p1_text = self.font_large.render(str(power1), True, (255, 255, 255))
            p2_text = self.font_large.render(str(power2), True, (255, 255, 255))
            screen.blit(p1_text, (p1_rect.centerx - p1_text.get_width() // 2, p1_rect.bottom + 20))
            screen.blit(p2_text, (p2_rect.centerx - p2_text.get_width() // 2, p2_rect.bottom + 20))
        else:
            power1 = hero1.power if hero1 else 0
            power2 = hero2.power if hero2 else 0
            power_diff = abs(power1 - power2)
            
            if power1 > power2:
                color1, scale1 = (255, 255, 0), 1.2
                color2, scale2 = (255, 255, 255), 1.0
                diff1, diff2 = power_diff, 0
            elif power2 > power1:
                color1, scale1 = (255, 255, 255), 1.0
                color2, scale2 = (255, 255, 0), 1.2
                diff1, diff2 = 0, power_diff
            else:
                color1, scale1 = (255, 255, 255), 1.0
                color2, scale2 = (255, 255, 255), 1.0
                diff1, diff2 = 0, 0
            
            font_size1 = int(48 * scale1)
            font_size2 = int(48 * scale2)
            try:
                font1 = assets.load_font('assets/fonts/Monocraft.ttf', font_size1)
                font2 = assets.load_font('assets/fonts/Monocraft.ttf', font_size2)
                font_diff = assets.load_font('assets/fonts/Monocraft.ttf', 24)
            except:
                font1 = pygame.font.Font(None, font_size1)
                font2 = pygame.font.Font(None, font_size2)
                font_diff = pygame.font.Font(None, 24)
            
            p1_text = font1.render(str(power1), True, color1)
            p2_text = font2.render(str(power2), True, color2)
            screen.blit(p1_text, (p1_rect.centerx - p1_text.get_width() // 2, p1_rect.bottom + 20))
            screen.blit(p2_text, (p2_rect.centerx - p2_text.get_width() // 2, p2_rect.bottom + 20))
            
            diff1_text = font_diff.render(f"+{diff1}" if diff1 > 0 else "0", True, color1)
            diff2_text = font_diff.render(f"+{diff2}" if diff2 > 0 else "0", True, color2)
            screen.blit(diff1_text, (p1_rect.centerx - diff1_text.get_width() // 2, p1_rect.bottom + 85))
            screen.blit(diff2_text, (p2_rect.centerx - diff2_text.get_width() // 2, p2_rect.bottom + 85))
        
        if self.compare_finished:
            if int(self.blink_timer * 2) % 2 == 0:
                hint = self.font_normal.render("Press ENTER to continue", True, (200, 200, 200))
                screen.blit(hint, (SCREEN_WIDTH // 2 - hint.get_width() // 2, SCREEN_HEIGHT - 50))
    
    def _draw_round_result_phase(self, screen):
        """วาดผลรอบปัจจุบัน"""
        result = self.round_results[-1]
        
        box = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 150, 500, 300)
        pygame.draw.rect(screen, (30, 30, 30, 220), box)
        pygame.draw.rect(screen, (255, 255, 255), box, 3)
        
        round_text = f"ROUND {result['round']} RESULT"
        round_surf = self.font_title.render(round_text, True, (255, 255, 255))
        screen.blit(round_surf, (box.centerx - round_surf.get_width() // 2, box.y + 20))
        
        if result['winner'] == 1:
            winner_text = "PLAYER 1 WINS!"
            color = (255, 215, 0)
        elif result['winner'] == 2:
            winner_text = "PLAYER 2 WINS!"
            color = (255, 215, 0)
        else:
            winner_text = "DRAW!"
            color = (200, 200, 200)
        
        winner_surf = self.font_large.render(winner_text, True, color)
        screen.blit(winner_surf, (box.centerx - winner_surf.get_width() // 2, box.y + 80))
        
        score_text = f"Score: P1 {self.p1_wins} - {self.p2_wins} P2"
        score_surf = self.font_normal.render(score_text, True, (255, 255, 255))
        screen.blit(score_surf, (box.centerx - score_surf.get_width() // 2, box.y + 150))
        
        if int(self.blink_timer * 2) % 2 == 0:
            hint = self.font_normal.render("Press ENTER to continue", True, (200, 200, 200))
            screen.blit(hint, (box.centerx - hint.get_width() // 2, box.bottom - 40))
    
    def _draw_final_result_phase(self, screen):
        """วาดผลสุดท้าย"""
        box = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 150, 500, 300)
        pygame.draw.rect(screen, (30, 30, 30, 220), box)
        pygame.draw.rect(screen, (255, 255, 255), box, 3)
        
        if self.winner == 1:
            result_text = "PLAYER 1 WINS!"
            color = (255, 215, 0)
        elif self.winner == 2:
            result_text = "PLAYER 2 WINS!"
            color = (255, 215, 0)
        else:
            result_text = "DRAW!"
            color = (200, 200, 200)
        
        result = self.font_large.render(result_text, True, color)
        screen.blit(result, (box.centerx - result.get_width() // 2, box.y + 40))
        
        final_score = f"Final Score: {self.p1_wins} - {self.p2_wins}"
        score_surf = self.font_normal.render(final_score, True, (255, 255, 255))
        screen.blit(score_surf, (box.centerx - score_surf.get_width() // 2, box.y + 100))
        
        p1_score = self.font_normal.render(f"Player 1 Wins: {self.player1_data['rank']}", True, (255, 255, 255))
        screen.blit(p1_score, (box.centerx - p1_score.get_width() // 2, box.y + 140))
        
        p2_score = self.font_normal.render(f"Player 2 Wins: {self.player2_data['rank']}", True, (255, 255, 255))
        screen.blit(p2_score, (box.centerx - p2_score.get_width() // 2, box.y + 170))
        
        money_y = box.y + 210
        if self.winner == 1:
            p1_money = self.font_normal.render(f"Player 1: +{self.bet_amount} coins", True, (0, 255, 0))
            p2_money = self.font_normal.render(f"Player 2: -{self.bet_amount} coins", True, (255, 0, 0))
        elif self.winner == 2:
            p1_money = self.font_normal.render(f"Player 1: -{self.bet_amount} coins", True, (255, 0, 0))
            p2_money = self.font_normal.render(f"Player 2: +{self.bet_amount} coins", True, (0, 255, 0))
        else:
            p1_money = self.font_normal.render(f"Player 1: 0 coins", True, (200, 200, 200))
            p2_money = self.font_normal.render(f"Player 2: 0 coins", True, (200, 200, 200))
        
        screen.blit(p1_money, (box.centerx - p1_money.get_width() // 2, money_y))
        screen.blit(p2_money, (box.centerx - p2_money.get_width() // 2, money_y + 25))
        
        if int(self.blink_timer * 2) % 2 == 0:
            hint = self.font_normal.render("Press ENTER to continue", True, (150, 150, 150))
            screen.blit(hint, (box.centerx - hint.get_width() // 2, box.bottom - 30))
    
    def exit(self):
        pass
