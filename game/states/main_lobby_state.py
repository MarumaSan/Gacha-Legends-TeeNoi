"""Main lobby state - central hub with navigation to all game features"""

import pygame
from game.game_state import GameState
from game.ui.button import Button
from game.ui.text_display import TextDisplay
from game.systems.asset_manager import AssetManager
from game.data.player_data import PlayerData
from game.data.hero_data import get_hero
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GOLD


class MainLobbyState(GameState):
    """Main lobby screen with navigation to Profile, Box, Book, Settings, and Exit"""
    
    def __init__(self, game, player_data: PlayerData):
        """
        Initialize the main lobby state
        
        Args:
            game: Reference to the main Game instance
            player_data: PlayerData instance for accessing player information
        """
        super().__init__(game)
        self.assets = AssetManager()
        self.player_data = player_data
        self.background = None
        self.font_large = None
        self.font_normal = None
        
        # ปุ่มต่างๆ ในหน้า lobby
        self.profile_button = None  # ปุ่ม Celestial Chest (ตรงกลาง)
        self.box_button = None  # ปุ่ม Mystic Chest (ซ้าย)
        self.book_button = None  # ปุ่ม Collection (ขวา)
        self.settings_button = None  # ปุ่ม Settings (มุมขวาบน)
        
        # กรอบและรูปภาพด้านบน
        self.profile_frame = None  # กรอบ profile ตรงกลางบน
        self.coin_image = None  # รูปเหรียญ
        self.profile_image = None  # รูป profile (กดได้ไปหน้า profile)
        self.profile_image_rect = None  # พื้นที่สำหรับตรวจจับการคลิก profile
        self.add_code_image = None  # ปุ่ม add code (กดได้ไปหน้า settings)
        self.add_code_image_rect = None  # พื้นที่สำหรับตรวจจับการคลิก add code
        
        # รูปตัวละครตรงกลาง
        self.hero_portraits = []  # รูปตัวละคร (สูงสุด 3 ตัว)
        self.portrait_positions = []  # ตำแหน่งของรูปตัวละคร
        self.hero_ids_displayed = []  # ID ของตัวละครที่แสดง
        self.selected_hero_for_detail = None  # ตัวละครที่เลือกเพื่อดูรายละเอียด
    
    def enter(self):
        """เรียกเมื่อเข้าสู่หน้านี้ - โหลดรูปภาพและสร้าง UI"""
        # โหลดภาพพื้นหลัง
        try:
            self.background = self.assets.load_image('assets/backgrounds/town_1.png', 
                                                     (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Warning: Could not load background: {e}")
            # Create a fallback background
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((60, 80, 100))
        
        # โหลดฟอนต์
        try:
            self.font_large = self.assets.load_font('assets/fonts/Monocraft.ttf', 32)
            self.font_normal = self.assets.load_font('assets/fonts/Monocraft.ttf', 24)
        except Exception as e:
            print(f"Warning: Could not load font: {e}")
            self.font_large = pygame.font.Font(None, 32)
            self.font_normal = pygame.font.Font(None, 24)
        
        # โหลดกรอบ profile (ขนาดต้นฉบับ)
        try:
            self.profile_frame = self.assets.load_image('assets/ui/profile frame.png')
        except Exception as e:
            print(f"Warning: Could not load profile frame: {e}")
            self.profile_frame = None
        
        # โหลดรูปเหรียญ (ขนาดต้นฉบับ)
        try:
            self.coin_image = self.assets.load_image('assets/ui/coin.png')
        except Exception as e:
            print(f"Warning: Could not load coin image: {e}")
            self.coin_image = None
        
        # โหลดรูป profile (ขนาดต้นฉบับ)
        try:
            self.profile_image = self.assets.load_image('assets/ui/profile.png')
        except Exception as e:
            print(f"Warning: Could not load profile image: {e}")
            self.profile_image = None
        
        # โหลดรูปปุ่ม add code (ขนาดต้นฉบับ)
        try:
            self.add_code_image = self.assets.load_image('assets/ui/add code.png')
        except Exception as e:
            print(f"Warning: Could not load add code image: {e}")
            self.add_code_image = None
        
        # สร้างปุ่มต่างๆ
        self._create_buttons()
        
        # โหลดรูปตัวละคร
        self._load_hero_portraits()
    
    def _create_buttons(self):
        """สร้างปุ่ม chest และ collection พร้อมรูปภาพ"""
        # โหลดรูป chest และ collection (ขนาดเล็กลง)
        try:
            mystic_chest_img = self.assets.load_image('assets/ui/mystic chest.png', (120, 120))
            celestial_chest_img = self.assets.load_image('assets/ui/celestial chest.png', (120, 120))
            collection_img = self.assets.load_image('assets/ui/collection.png', (120, 120))
        except Exception as e:
            print(f"Warning: Could not load chest/collection images: {e}")
            mystic_chest_img = None
            celestial_chest_img = None
            collection_img = None
        
        # ขนาดและตำแหน่งของปุ่ม
        button_width = 120
        button_height = 120  # ขนาดเท่ากับรูป
        button_spacing = 30  # ระยะห่างระหว่างปุ่ม
        
        # คำนวณตำแหน่งสำหรับพื้นที่ด้านล่าง
        bottom_y = SCREEN_HEIGHT - 160
        center_x = SCREEN_WIDTH // 2
        
        # ปุ่ม Mystic Chest (ซ้าย)
        self.box_button = Button(
            x=center_x - button_width - button_spacing - button_width // 2,
            y=bottom_y,
            width=button_width,
            height=button_height,
            text="",
            image=mystic_chest_img,
            callback=lambda: self.on_box_click('mystic'),
            font=self.font_normal,
            text_color=(255, 255, 255),
            bg_color=(40, 30, 20),
            hover_color=(60, 50, 40)
        )
        
        # ปุ่ม Celestial Chest (กลาง)
        self.profile_button = Button(
            x=center_x - button_width // 2,
            y=bottom_y,
            width=button_width,
            height=button_height,
            text="",
            image=celestial_chest_img,
            callback=lambda: self.on_box_click('celestial'),
            font=self.font_normal,
            text_color=(255, 255, 255),
            bg_color=(40, 30, 20),
            hover_color=(60, 50, 40)
        )
        
        # ปุ่ม Collection (ขวา)
        self.book_button = Button(
            x=center_x + button_width // 2 + button_spacing,
            y=bottom_y,
            width=button_width,
            height=button_height,
            text="",
            image=collection_img,
            callback=self.on_book_click,
            font=self.font_normal,
            text_color=(255, 255, 255),
            bg_color=(40, 30, 20),
            hover_color=(60, 50, 40)
        )
        
        # โหลดรูปปุ่ม settings
        try:
            settings_img = self.assets.load_image('assets/ui/setting.png', (50, 50))
        except Exception as e:
            print(f"Warning: Could not load settings image: {e}")
            settings_img = None
        
        # ปุ่ม Settings (มุมขวาบน, ไม่มี hover effect)
        self.settings_button = Button(
            x=SCREEN_WIDTH - 60,
            y=20,
            width=50,
            height=50,
            text="",
            image=settings_img,
            callback=self.on_settings_click,
            font=self.font_large,
            text_color=(255, 255, 255),
            bg_color=(0, 0, 0, 0),
            hover_color=(0, 0, 0, 0)
        )
        


    def _load_hero_portraits(self):
        """โหลดและจัดตำแหน่งรูปตัวละครที่มี (สูงสุด 3 ตัว)"""
        self.hero_portraits = []
        self.portrait_positions = []
        self.hero_ids_displayed = []
        
        # ดึงตัวละครที่มีและเรียงตามความแรร์ (แรร์สุดก่อน)
        owned_hero_ids = list(self.player_data.owned_heroes)
        
        # เรียงตามความแรร์ (จากมากไปน้อย - แรร์สุดก่อน)
        hero_rarity_map = {
            'rare': 1,
            'epic': 2,
            'legendary': 3,
            'extreme': 4
        }
        
        def get_hero_rarity_value(hero_id):
            hero = get_hero(hero_id)
            if hero:
                return hero_rarity_map.get(hero.rarity.lower(), 0)
            return 0
        
        owned_hero_ids.sort(key=get_hero_rarity_value, reverse=True)
        
        # จำกัดแค่ 3 ตัวแรกสำหรับแสดง
        owned_hero_ids = owned_hero_ids[:3]
        
        if not owned_hero_ids:
            # ยังไม่มีตัวละคร
            return
        
        # ตั้งค่าการแสดงรูปตัวละคร
        portrait_spacing = 60
        center_y = SCREEN_HEIGHT // 2 - 50
        
        # โหลดรูปตัวละครด้วยขนาดต่างกัน (ตัวกลางใหญ่กว่า, ข้างๆเล็กกว่า)
        temp_portraits = []
        for i, hero_id in enumerate(owned_hero_ids):
            hero = get_hero(hero_id)
            if hero:
                try:
                    # Load original image first
                    original_portrait = self.assets.load_image(hero.portrait_path)
                    # Get original dimensions
                    original_width = original_portrait.get_width()
                    original_height = original_portrait.get_height()
                    
                    # ขนาดต่างกันระหว่างตัวกลางกับข้างๆ
                    if len(owned_hero_ids) == 3 and i == 1:
                        # ตัวกลาง - ขนาด 40%
                        scale = 0.4
                    elif len(owned_hero_ids) == 1:
                        # มีแค่ตัวเดียว - ขนาด 40%
                        scale = 0.4
                    else:
                        # ตัวข้างๆ - ขนาด 30% (เล็กกว่า)
                        scale = 0.3
                    
                    scaled_width = int(original_width * scale)
                    scaled_height = int(original_height * scale)
                    portrait = pygame.transform.scale(original_portrait, (scaled_width, scaled_height))
                    temp_portraits.append(portrait)
                    self.hero_ids_displayed.append(hero_id)
                except Exception as e:
                    print(f"Warning: Could not load portrait for hero {hero_id}: {e}")
        
        if not temp_portraits:
            return
        
        # คำนวณตำแหน่งตามจำนวนตัวละคร
        if len(temp_portraits) == 1:
            # มี 1 ตัว - แสดงตรงกลาง
            portrait = temp_portraits[0]
            width = portrait.get_width()
            height = portrait.get_height()
            positions = [(SCREEN_WIDTH // 2 - width // 2, center_y - height // 2)]
        elif len(temp_portraits) == 2:
            # มี 2 ตัว - แสดงทั้งสองข้าง
            positions = []
            for i, portrait in enumerate(temp_portraits):
                width = portrait.get_width()
                height = portrait.get_height()
                if i == 0:
                    x = SCREEN_WIDTH // 2 - width - portrait_spacing // 2
                else:
                    x = SCREEN_WIDTH // 2 + portrait_spacing // 2
                y = center_y - height // 2
                positions.append((x, y))
        else:
            # มี 3 ตัว - กระจายเท่าๆ กัน
            positions = []
            for i, portrait in enumerate(temp_portraits):
                width = portrait.get_width()
                height = portrait.get_height()
                if i == 0:
                    # Left
                    x = SCREEN_WIDTH // 2 - width - portrait_spacing - width // 2
                elif i == 1:
                    # Center
                    x = SCREEN_WIDTH // 2 - width // 2
                else:
                    # Right
                    x = SCREEN_WIDTH // 2 + portrait_spacing + width // 2
                y = center_y - height // 2
                positions.append((x, y))
        
        self.hero_portraits = temp_portraits
        self.portrait_positions = positions
    

    def on_box_click(self, chest_type='mystic'):
        """เมื่อกดปุ่ม Chest - ไปหน้าสุ่มตามประเภท"""
        if chest_type == 'mystic':
            print("Mystic Chest clicked - navigating to Mystic Chest")
            self.game.change_state('mystic_chest')
        elif chest_type == 'celestial':
            print("Celestial Chest clicked - navigating to Celestial Chest")
            self.game.change_state('celestial_chest')
        else:
            print(f"{chest_type.capitalize()} Chest clicked - navigating to Gacha")
            self.game.selected_chest_type = chest_type
            self.game.change_state('gacha')
    
    def on_book_click(self):
        """เมื่อกดปุ่ม Collection - ไปหน้า Book"""
        print("Book button clicked - navigating to Book")
        self.game.change_state('book')
    
    def on_settings_click(self):
        """เมื่อกดปุ่ม Settings - ไปหน้า Settings"""
        print("Settings button clicked - navigating to Settings")
        self.game.previous_state = 'main_lobby'
        self.game.change_state('settings')
    
    def handle_event(self, event):
        """
        จัดการ event ต่างๆ (คลิก, กดปุ่ม)
        
        Args:
            event: pygame.event.Event object
        """
        # ส่งต่อ event ไปยังปุ่มต่างๆ
        if self.profile_button:
            self.profile_button.handle_event(event)
        if self.box_button:
            self.box_button.handle_event(event)
        if self.book_button:
            self.book_button.handle_event(event)
        if self.settings_button:
            self.settings_button.handle_event(event)
        
        # จัดการการคลิกรูป profile
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            if self.profile_image_rect and self.profile_image_rect.collidepoint(mouse_pos):
                # คลิก profile - ไปหน้า profile
                print("Profile clicked - navigating to Profile")
                self.game.change_state('profile')
                return
            
            # จัดการการคลิกปุ่ม add code
            if self.add_code_image_rect and self.add_code_image_rect.collidepoint(mouse_pos):
                # คลิก add code - ไปหน้า add_code
                print("Add Code clicked - navigating to Add Code")
                self.game.previous_state = 'main_lobby'
                self.game.change_state('add_code')
                return
        
        # จัดการการคลิกรูปตัวละคร
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for i, (portrait, pos) in enumerate(zip(self.hero_portraits, self.portrait_positions)):
                # สร้าง rect สำหรับรูปตัวละคร
                width = portrait.get_width()
                height = portrait.get_height()
                hero_rect = pygame.Rect(pos[0], pos[1], width, height)
                if hero_rect.collidepoint(mouse_pos):
                    # คลิกตัวละคร - ไปหน้า collection และแสดงรายละเอียด
                    hero_id = self.hero_ids_displayed[i]
                    self.game.selected_hero_id = hero_id
                    self.game.change_state('book')
    
    def update(self, dt):
        """
        อัปเดตสถานะของเกม
        
        Args:
            dt: เวลาที่ผ่านไปตั้งแต่ครั้งล่าสุด (วินาที)
        """
        # อัปเดตปุ่มต่างๆ
        if self.box_button:
            self.box_button.update(dt)
        if self.profile_button:
            self.profile_button.update(dt)
        if self.book_button:
            self.book_button.update(dt)
        if self.settings_button:
            self.settings_button.update(dt)
    
    def draw(self, screen):
        """
        วาดหน้า main lobby ลงบนหน้าจอ
        
        Args:
            screen: pygame.Surface สำหรับวาด
        """
        # วาดพื้นหลัง
        if self.background:
            screen.blit(self.background, (0, 0))
        
        # วาดกรอบ profile ตรงกลางบน
        if self.profile_frame:
            frame_width = self.profile_frame.get_width()
            frame_x = SCREEN_WIDTH // 2 - frame_width // 2
            frame_y = 20
            screen.blit(self.profile_frame, (frame_x, frame_y))
        
        # วาดรูป profile ด้านบน (ระดับเดียวกับกรอบ, ทางซ้าย)
        if self.profile_image and self.profile_frame:
            frame_width = self.profile_frame.get_width()
            frame_x = SCREEN_WIDTH // 2 - frame_width // 2
            frame_y = 20
            
            profile_width = self.profile_image.get_width()
            profile_height = self.profile_image.get_height()
            
            # วางตำแหน่งรูป profile ให้ทับขอบซ้ายของกรอบ
            profile_x = frame_x - profile_width + 85  # Move right to overlap frame edge (90 - 5)
            profile_y = frame_y + 11  # Move down slightly (10 + 1)
            
            screen.blit(self.profile_image, (profile_x, profile_y))
            
            # เก็บพื้นที่รูป profile สำหรับตรวจจับการคลิก
            self.profile_image_rect = pygame.Rect(profile_x, profile_y, profile_width, profile_height)
        
        # วาดปุ่ม add code ด้านบน (ระดับเดียวกับกรอบ, ทางขวา)
        if self.add_code_image and self.profile_frame:
            frame_width = self.profile_frame.get_width()
            frame_x = SCREEN_WIDTH // 2 - frame_width // 2
            frame_y = 20
            
            add_code_width = self.add_code_image.get_width()
            add_code_height = self.add_code_image.get_height()
            
            # วางตำแหน่งปุ่ม add code ให้ทับขอบขวาของกรอบ (กระจกเงาของ profile)
            add_code_x = frame_x + frame_width - 75  # Move left to overlap frame edge (80 - 5 = 75, moving right)
            add_code_y = frame_y + 14  # Move down slightly
            
            screen.blit(self.add_code_image, (add_code_x, add_code_y))
            
            # เก็บพื้นที่ปุ่ม add code สำหรับตรวจจับการคลิก
            self.add_code_image_rect = pygame.Rect(add_code_x, add_code_y, add_code_width, add_code_height)
        
        # วาดรูปเหรียญในพื้นที่สีดำของกรอบ profile (ทางขวา, กึ่งกลางแนวตั้ง)
        if self.coin_image and self.profile_frame:
            frame_width = self.profile_frame.get_width()
            frame_height = self.profile_frame.get_height()
            frame_x = SCREEN_WIDTH // 2 - frame_width // 2
            frame_y = 20
            
            coin_width = self.coin_image.get_width()
            coin_height = self.coin_image.get_height()
            
            # วางตำแหน่งเหรียญที่ขอบขวาของพื้นที่สีดำ, กึ่งกลางแนวตั้ง
            # สมมติว่าพื้นที่สีดำมี padding จากขอบกรอบ
            black_area_padding = 90  # ปรับค่านี้ตามการออกแบบกรอบจริง
            coin_x = frame_x + frame_width - coin_width - black_area_padding
            coin_y = frame_y + (frame_height - coin_height) // 2
            
            screen.blit(self.coin_image, (coin_x, coin_y))
            
            # วาดข้อความจำนวนเหรียญหน้าเหรียญ
            coin_amount = self.player_data.get_coin_balance()
            coin_text = self.font_normal.render(str(coin_amount), True, (255, 255, 255))  # สีขาว, ฟอนต์เล็ก
            text_width = coin_text.get_width()
            text_height = coin_text.get_height()
            
            # วางตำแหน่งข้อความทางซ้ายของเหรียญ, กึ่งกลางแนวตั้ง
            text_x = coin_x - text_width - 10  # ห่างจากเหรียญ 10px
            text_y = coin_y + (coin_height - text_height) // 2
            
            screen.blit(coin_text, (text_x, text_y))
        
        # วาดรูปตัวละคร (ไม่มี hover effect)
        for i, (portrait, position) in enumerate(zip(self.hero_portraits, self.portrait_positions)):
            screen.blit(portrait, position)
        
        # Draw buttons
        if self.profile_button:
            self.profile_button.draw(screen)
        if self.box_button:
            self.box_button.draw(screen)
        if self.book_button:
            self.book_button.draw(screen)
        if self.settings_button:
            self.settings_button.draw(screen)
    

    def exit(self):
        """Called when exiting this state"""
        pass
