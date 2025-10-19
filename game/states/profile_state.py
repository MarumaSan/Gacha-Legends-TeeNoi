"""Profile state - display player statistics and owned heroes"""

import pygame
from game.game_state import GameState
from game.ui.button import Button
from game.ui.text_display import TextDisplay
from game.systems.asset_manager import AssetManager
from game.data.player_data import PlayerData
from game.data.hero_data import get_hero, get_all_heroes
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_GOLD, COLOR_WHITE


class ProfileState(GameState):
    """Profile screen showing player stats and owned heroes"""
    
    def __init__(self, game, player_data: PlayerData):
        """
        Initialize the profile state
        
        Args:
            game: Reference to the main Game instance
            player_data: PlayerData instance for accessing player information
        """
        super().__init__(game)
        self.assets = AssetManager()
        self.player_data = player_data
        self.background = None
        self.font_title = None
        self.font_large = None
        self.font_normal = None
        
        # UI elements
        self.back_button = None
        self.power_display = None
        self.rank_display = None
        self.coin_display = None
        
        # Hero grid
        self.hero_portraits = []
        self.hero_portrait_rects = []
        self.heroes_per_row = 5
        self.heroes_per_page = 15
    
    def enter(self):
        """Called when entering this state - load assets and create UI"""
        # Load background (book-style interface)
        try:
            self.background = self.assets.load_image('assets/backgrounds/book.png', 
                                                     (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Warning: Could not load background: {e}")
            # Create a fallback background
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((40, 30, 20))
        
        # Load fonts
        try:
            self.font_title = self.assets.load_font('assets/fonts/Monocraft.ttf', 48)
            self.font_large = self.assets.load_font('assets/fonts/Monocraft.ttf', 32)
            self.font_normal = self.assets.load_font('assets/fonts/Monocraft.ttf', 24)
        except Exception as e:
            print(f"Warning: Could not load font: {e}")
            self.font_title = pygame.font.Font(None, 48)
            self.font_large = pygame.font.Font(None, 32)
            self.font_normal = pygame.font.Font(None, 24)
        
        # Create stat displays
        self._create_stat_displays()
        
        # Load hero portraits
        self._load_hero_grid()
        
        # Create back button
        self.back_button = Button(
            x=SCREEN_WIDTH // 2 - 100,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=60,
            text="Return",
            callback=self.on_back_click,
            font=self.font_normal,
            text_color=(255, 255, 255),
            bg_color=(70, 70, 120),
            hover_color=(100, 100, 150)
        )
    
    def _create_stat_displays(self):
        """Create text displays for player statistics"""
        # Calculate total power
        total_power = self._calculate_total_power()
        
        # Get rank (placeholder for now)
        rank = self.player_data.rank if self.player_data.rank > 0 else "Unranked"
        
        # Get coin balance
        coins = self.player_data.get_coin_balance()
        
        # Position stats in the upper portion of the screen
        stats_start_y = 150
        stats_spacing = 50
        center_x = SCREEN_WIDTH // 2
        
        # Power level display
        self.power_display = TextDisplay(
            text=f"Power Level: {total_power}",
            font=self.font_large,
            color=COLOR_GOLD,
            position=(center_x - 150, stats_start_y)
        )
        
        # Rank display
        self.rank_display = TextDisplay(
            text=f"Rank: {rank}",
            font=self.font_normal,
            color=COLOR_WHITE,
            position=(center_x - 100, stats_start_y + stats_spacing)
        )
        
        # Coin balance display
        self.coin_display = TextDisplay(
            text=f"Coins: {coins}",
            font=self.font_normal,
            color=COLOR_GOLD,
            position=(center_x - 100, stats_start_y + stats_spacing * 2)
        )
    
    def _calculate_total_power(self) -> int:
        """
        Calculate total power from all owned heroes
        
        Returns:
            int: Total power level
        """
        total_power = 0
        for hero_id in self.player_data.owned_heroes:
            hero = get_hero(hero_id)
            if hero:
                total_power += hero.power
        return total_power
    
    def _load_hero_grid(self):
        """Load and position hero portraits in a grid"""
        self.hero_portraits = []
        self.hero_portrait_rects = []
        
        # Get all owned heroes
        owned_hero_ids = sorted(list(self.player_data.owned_heroes))
        
        if not owned_hero_ids:
            # No heroes owned yet
            return
        
        # Grid settings
        portrait_size = 100
        padding = 20
        grid_start_x = SCREEN_WIDTH // 2 - (self.heroes_per_row * (portrait_size + padding)) // 2
        grid_start_y = 320
        
        # Load portraits for owned heroes (limit to first page)
        for i, hero_id in enumerate(owned_hero_ids[:self.heroes_per_page]):
            hero = get_hero(hero_id)
            if hero:
                try:
                    portrait = self.assets.load_image(hero.portrait_path, (portrait_size, portrait_size))
                    self.hero_portraits.append((portrait, hero))
                    
                    # Calculate grid position
                    row = i // self.heroes_per_row
                    col = i % self.heroes_per_row
                    x = grid_start_x + col * (portrait_size + padding)
                    y = grid_start_y + row * (portrait_size + padding)
                    
                    rect = pygame.Rect(x, y, portrait_size, portrait_size)
                    self.hero_portrait_rects.append(rect)
                except Exception as e:
                    print(f"Warning: Could not load portrait for hero {hero_id}: {e}")
    
    def on_back_click(self):
        """Callback for Return button - go back to main lobby"""
        print("Return button clicked - going back to main lobby")
        self.game.change_state('main_lobby')
    
    def handle_event(self, event):
        """
        Handle pygame events
        
        Args:
            event: pygame.event.Event object
        """
        # Handle back button
        if self.back_button:
            self.back_button.handle_event(event)
    
    def update(self, dt):
        """
        Update game state logic
        
        Args:
            dt: Delta time in seconds since last update
        """
        # Update back button
        if self.back_button:
            self.back_button.update(dt)
        
        # Update stat displays with current values
        if self.power_display:
            total_power = self._calculate_total_power()
            self.power_display.set_text(f"Power Level: {total_power}")
        
        if self.coin_display:
            coins = self.player_data.get_coin_balance()
            self.coin_display.set_text(f"Coins: {coins}")
    
    def draw(self, screen):
        """
        Draw the profile state to the screen
        
        Args:
            screen: pygame.Surface to draw on
        """
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
        
        # Draw title
        if self.font_title:
            title_surface = self.font_title.render("Profile", True, COLOR_WHITE)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
            screen.blit(title_surface, title_rect)
        
        # Draw stat displays
        if self.power_display:
            self.power_display.draw(screen)
        if self.rank_display:
            self.rank_display.draw(screen)
        if self.coin_display:
            self.coin_display.draw(screen)
        
        # Draw "Owned Heroes" label
        if self.font_normal:
            label_surface = self.font_normal.render("Owned Heroes", True, COLOR_WHITE)
            label_rect = label_surface.get_rect(center=(SCREEN_WIDTH // 2, 280))
            screen.blit(label_surface, label_rect)
        
        # Draw hero portraits
        for (portrait, hero), rect in zip(self.hero_portraits, self.hero_portrait_rects):
            screen.blit(portrait, rect)
            
            # Draw border around portrait
            pygame.draw.rect(screen, COLOR_WHITE, rect, 2)
        
        # Draw "no heroes" message if player has no heroes
        if not self.hero_portraits and self.font_normal:
            no_heroes_text = self.font_normal.render("No heroes owned yet", True, (150, 150, 150))
            no_heroes_rect = no_heroes_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
            screen.blit(no_heroes_text, no_heroes_rect)
        
        # Draw back button
        if self.back_button:
            self.back_button.draw(screen)
    
    def exit(self):
        """Called when exiting this state"""
        pass
