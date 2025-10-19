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
        
        # UI elements
        self.profile_button = None
        self.box_button = None
        self.book_button = None
        self.settings_button = None
        self.exit_button = None
        self.coin_display = None
        self.add_code_button = None
        
        # Top bar UI assets
        self.profile_image = None
        self.profile_frame = None
        self.coin_bg_image = None
        self.add_code_button_image = None
        
        # Hero portraits
        self.hero_portraits = []
        self.portrait_positions = []
        self.hero_ids_displayed = []
        self.selected_hero_for_detail = None
    
    def enter(self):
        """Called when entering this state - load assets and create UI"""
        # Load background
        try:
            self.background = self.assets.load_image('assets/backgrounds/town_2.png', 
                                                     (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Warning: Could not load background: {e}")
            # Create a fallback background
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((60, 80, 100))
        
        # Load fonts
        try:
            self.font_large = self.assets.load_font('assets/fonts/Monocraft.ttf', 32)
            self.font_normal = self.assets.load_font('assets/fonts/Monocraft.ttf', 24)
        except Exception as e:
            print(f"Warning: Could not load font: {e}")
            self.font_large = pygame.font.Font(None, 32)
            self.font_normal = pygame.font.Font(None, 24)
        
        # Create navigation buttons
        self._create_buttons()
        
        # Create coin display
        self._create_coin_display()
        
        # Load hero portraits
        self._load_hero_portraits()
    
    def _create_buttons(self):
        """Create chest and collection buttons with images"""
        # Load chest and collection images
        try:
            mystic_chest_img = self.assets.load_image('assets/ui/Mystic Chest.png', (180, 180))
            celestial_chest_img = self.assets.load_image('assets/ui/Celestial Chest.png', (180, 180))
            collection_img = self.assets.load_image('assets/ui/COLLECTION.png', (180, 180))
        except Exception as e:
            print(f"Warning: Could not load chest/collection images: {e}")
            mystic_chest_img = None
            celestial_chest_img = None
            collection_img = None
        
        # Button dimensions and positions
        button_width = 180
        button_height = 230  # Taller to include image + label
        button_spacing = 40
        
        # Calculate positions for bottom area
        bottom_y = SCREEN_HEIGHT - 260
        center_x = SCREEN_WIDTH // 2
        
        # Mystic Chest button
        self.box_button = Button(
            x=center_x - button_width - button_spacing - button_width // 2,
            y=bottom_y,
            width=button_width,
            height=button_height,
            text="MYSTIC CHEST",
            image=mystic_chest_img,
            callback=lambda: self.on_box_click('mystic'),
            font=self.font_normal,
            text_color=(255, 255, 255),
            bg_color=(40, 30, 20),
            hover_color=(60, 50, 40)
        )
        
        # Celestial Chest button
        self.profile_button = Button(
            x=center_x - button_width // 2,
            y=bottom_y,
            width=button_width,
            height=button_height,
            text="CELESTIAL CHEST",
            image=celestial_chest_img,
            callback=lambda: self.on_box_click('celestial'),
            font=self.font_normal,
            text_color=(255, 255, 255),
            bg_color=(40, 30, 20),
            hover_color=(60, 50, 40)
        )
        
        # Collection button
        self.book_button = Button(
            x=center_x + button_width // 2 + button_spacing,
            y=bottom_y,
            width=button_width,
            height=button_height,
            text="COLLECTION",
            image=collection_img,
            callback=self.on_book_click,
            font=self.font_normal,
            text_color=(255, 255, 255),
            bg_color=(40, 30, 20),
            hover_color=(60, 50, 40)
        )
        
        # Settings and Exit buttons (smaller, at corners)
        self.settings_button = Button(
            x=SCREEN_WIDTH - 70,
            y=20,
            width=50,
            height=50,
            text="⚙",
            callback=self.on_settings_click,
            font=self.font_large,
            text_color=(255, 255, 255),
            bg_color=(70, 70, 120),
            hover_color=(100, 100, 150)
        )
        
        self.exit_button = Button(
            x=SCREEN_WIDTH - 70,
            y=80,
            width=50,
            height=50,
            text="✕",
            callback=self.on_exit_click,
            font=self.font_large,
            text_color=(255, 255, 255),
            bg_color=(120, 70, 70),
            hover_color=(150, 100, 100)
        )
    
    def _create_coin_display(self):
        """Create the top bar with profile, coins, and add code button"""
        # Load UI assets
        try:
            # Profile image
            self.profile_image = self.assets.load_image('assets/ui/profile.png', (80, 80))
            # Frame for profile
            self.profile_frame = self.assets.load_image('assets/ui/frame profile.png', (100, 100))
            # Coin background image
            self.coin_bg_image = self.assets.load_image('assets/ui/coin.png', (300, 80))
            # Add code button
            self.add_code_button_image = self.assets.load_image('assets/ui/add code.png', (60, 60))
        except Exception as e:
            print(f"Warning: Could not load UI assets: {e}")
            self.profile_image = None
            self.profile_frame = None
            self.coin_bg_image = None
            self.add_code_button_image = None
        
        # Create add code button
        self.add_code_button = Button(
            x=580,
            y=20,
            width=60,
            height=60,
            text="",
            image=self.add_code_button_image,
            callback=self.on_add_code_click,
            font=self.font_normal,
            text_color=COLOR_GOLD,
            bg_color=(0, 0, 0, 0),
            hover_color=(255, 255, 255, 50)
        )
        
        # Coin display text (will be drawn on top of coin background)
        self.coin_display = TextDisplay(
            text=f"{self.player_data.get_coin_balance()}",
            font=self.font_large,
            color=COLOR_GOLD,
            position=(420, 50),
            align='center'
        )
    
    def _load_hero_portraits(self):
        """Load and position hero portraits for owned heroes (3 heroes, center one larger)"""
        self.hero_portraits = []
        self.portrait_positions = []
        self.hero_ids_displayed = []
        
        # Get owned heroes (limit to first 3 for display)
        owned_hero_ids = list(self.player_data.owned_heroes)[:3]
        
        if not owned_hero_ids:
            # No heroes owned yet
            return
        
        # Portrait display settings
        side_portrait_size = 150
        center_portrait_size = 200
        portrait_spacing = 80
        center_y = SCREEN_HEIGHT // 2 - 50
        
        # Calculate positions for 3 heroes
        if len(owned_hero_ids) == 1:
            # Only 1 hero - show in center
            positions = [(SCREEN_WIDTH // 2 - center_portrait_size // 2, center_y - center_portrait_size // 2)]
            sizes = [center_portrait_size]
        elif len(owned_hero_ids) == 2:
            # 2 heroes - show both at sides
            positions = [
                (SCREEN_WIDTH // 2 - side_portrait_size - portrait_spacing, center_y - side_portrait_size // 2),
                (SCREEN_WIDTH // 2 + portrait_spacing, center_y - side_portrait_size // 2)
            ]
            sizes = [side_portrait_size, side_portrait_size]
        else:
            # 3 heroes - left (small), center (large), right (small)
            positions = [
                (SCREEN_WIDTH // 2 - center_portrait_size // 2 - side_portrait_size - portrait_spacing, 
                 center_y - side_portrait_size // 2 + 25),
                (SCREEN_WIDTH // 2 - center_portrait_size // 2, center_y - center_portrait_size // 2),
                (SCREEN_WIDTH // 2 + center_portrait_size // 2 + portrait_spacing, 
                 center_y - side_portrait_size // 2 + 25)
            ]
            sizes = [side_portrait_size, center_portrait_size, side_portrait_size]
        
        # Load portraits for owned heroes
        for i, hero_id in enumerate(owned_hero_ids):
            hero = get_hero(hero_id)
            if hero:
                try:
                    size = sizes[i]
                    portrait = self.assets.load_image(hero.portrait_path, (size, size))
                    self.hero_portraits.append(portrait)
                    self.portrait_positions.append(positions[i])
                    self.hero_ids_displayed.append(hero_id)
                except Exception as e:
                    print(f"Warning: Could not load portrait for hero {hero_id}: {e}")
    
    def update_coin_display(self):
        """Update the coin display with current balance"""
        if self.coin_display:
            self.coin_display.set_text(f"{self.player_data.get_coin_balance()}")
    
    def on_box_click(self, chest_type='mystic'):
        """Callback for Chest button - navigate to Gacha page with selected chest"""
        print(f"{chest_type.capitalize()} Chest clicked - navigating to Gacha")
        self.game.selected_chest_type = chest_type
        self.game.change_state('gacha')
    
    def on_book_click(self):
        """Callback for Book button - navigate to Book page"""
        print("Book button clicked - navigating to Book")
        self.game.change_state('book')
    
    def on_add_code_click(self):
        """Callback for Add Code button - navigate to Settings for code redemption"""
        print("Add Code button clicked - navigating to Settings")
        self.game.previous_state = 'main_lobby'
        self.game.change_state('settings')
    
    def on_settings_click(self):
        """Callback for Settings button - navigate to Settings page"""
        print("Settings button clicked - navigating to Settings")
        self.game.previous_state = 'main_lobby'
        self.game.change_state('settings')
    
    def on_exit_click(self):
        """Callback for Exit button - close the game"""
        print("Exit button clicked - closing game")
        self.game.quit()
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: pygame.event.Event object
        """
        # Delegate to buttons
        if self.add_code_button:
            self.add_code_button.handle_event(event)
        if self.profile_button:
            self.profile_button.handle_event(event)
        if self.box_button:
            self.box_button.handle_event(event)
        if self.book_button:
            self.book_button.handle_event(event)
        if self.settings_button:
            self.settings_button.handle_event(event)
        if self.exit_button:
            self.exit_button.handle_event(event)
        
        # Handle hero portrait clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for i, (portrait, pos) in enumerate(zip(self.hero_portraits, self.portrait_positions)):
                # Create rect for hero portrait
                size = portrait.get_width()
                hero_rect = pygame.Rect(pos[0], pos[1], size, size)
                if hero_rect.collidepoint(mouse_pos):
                    # Hero clicked - go to collection and show detail
                    hero_id = self.hero_ids_displayed[i]
                    self.game.selected_hero_id = hero_id
                    self.game.change_state('book')
    
    def update(self, dt):
        """
        Update game state logic
        
        Args:
            dt: Delta time in seconds since last update
        """
        # Update buttons
        if self.add_code_button:
            self.add_code_button.update(dt)
        if self.box_button:
            self.box_button.update(dt)
        if self.profile_button:
            self.profile_button.update(dt)
        if self.book_button:
            self.book_button.update(dt)
        if self.settings_button:
            self.settings_button.update(dt)
        if self.exit_button:
            self.exit_button.update(dt)
        
        # Update coin display
        self.update_coin_display()
    
    def draw(self, screen):
        """
        Draw the main lobby state to the screen
        
        Args:
            screen: pygame.Surface to draw on
        """
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
        
        # Draw top bar UI
        self._draw_top_bar(screen)
        
        # Draw hero portraits with hover effect
        mouse_pos = pygame.mouse.get_pos()
        for i, (portrait, position) in enumerate(zip(self.hero_portraits, self.portrait_positions)):
            size = portrait.get_width()
            hero_rect = pygame.Rect(position[0], position[1], size, size)
            
            # Check if mouse is hovering
            if hero_rect.collidepoint(mouse_pos):
                # Draw glow effect
                glow_surface = pygame.Surface((size + 10, size + 10))
                glow_surface.fill((255, 215, 0))
                glow_surface.set_alpha(100)
                screen.blit(glow_surface, (position[0] - 5, position[1] - 5))
            
            screen.blit(portrait, position)
            
            # Draw border
            pygame.draw.rect(screen, COLOR_GOLD, hero_rect, 3)
        
        # Draw buttons
        if self.profile_button:
            self.profile_button.draw(screen)
        if self.box_button:
            self.box_button.draw(screen)
        if self.book_button:
            self.book_button.draw(screen)
        if self.settings_button:
            self.settings_button.draw(screen)
        if self.exit_button:
            self.exit_button.draw(screen)
    
    def _draw_top_bar(self, screen):
        """Draw the top bar with profile, coins, and add code button"""
        # Draw coin background image (behind everything)
        if self.coin_bg_image:
            screen.blit(self.coin_bg_image, (120, 20))
        else:
            # Fallback: draw a dark rectangle
            pygame.draw.rect(screen, (40, 30, 20), (120, 20, 300, 80))
            pygame.draw.rect(screen, (100, 80, 60), (120, 20, 300, 80), 3)
        
        # Draw profile image
        if self.profile_image:
            screen.blit(self.profile_image, (20, 20))
        else:
            # Fallback: draw a circle
            pygame.draw.circle(screen, (100, 100, 100), (60, 60), 40)
        
        # Draw profile frame on top
        if self.profile_frame:
            screen.blit(self.profile_frame, (10, 10))
        else:
            # Fallback: draw a border
            pygame.draw.rect(screen, COLOR_GOLD, (10, 10, 100, 100), 3)
        
        # Draw coin count text (centered in the coin background area)
        if self.coin_display:
            self.coin_display.draw(screen)
        
        # Draw add code button
        if self.add_code_button:
            self.add_code_button.draw(screen)
    
    def exit(self):
        """Called when exiting this state"""
        pass
