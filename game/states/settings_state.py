"""Settings state - game settings and code redemption"""

import pygame
from game.game_state import GameState
from game.ui.button import Button
from game.ui.slider import Slider
from game.ui.text_input import TextInput
from game.systems.asset_manager import AssetManager
from game.systems.code_manager import CodeManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT


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
        self.code_input = None
        self.redeem_button = None
        self.back_button = None
        self.exit_button = None
        self.font_title = None
        self.font_normal = None
        self.font_small = None
        
        # Message display
        self.message = ""
        self.message_color = (255, 255, 255)
        self.message_timer = 0
        self.message_duration = 3.0  # seconds
    
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
            self.font_normal = self.assets.load_font('assets/fonts/Monocraft.ttf', 24)
            self.font_small = self.assets.load_font('assets/fonts/Monocraft.ttf', 20)
        except Exception as e:
            print(f"Warning: Could not load font: {e}")
            self.font_title = pygame.font.Font(None, 48)
            self.font_normal = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 20)
        
        # Layout constants
        center_x = SCREEN_WIDTH // 2
        start_y = 200
        spacing = 100
        
        # Sound slider
        self.sound_slider = Slider(
            x=center_x - 100,
            y=start_y,
            width=300,
            height=20,
            min_value=0,
            max_value=100,
            initial_value=self.game.player_data.settings.get('volume', 50),
            callback=self.on_sound_change,
            label="Sound:",
            font=self.font_normal
        )
        
        # Code input field
        self.code_input = TextInput(
            x=center_x - 150,
            y=start_y + spacing,
            width=300,
            height=50,
            font=self.font_normal,
            placeholder="Enter code...",
            max_length=20,
            text_color=(255, 255, 255),
            bg_color=(50, 40, 30),
            active_color=(70, 60, 50)
        )
        
        # Redeem button
        self.redeem_button = Button(
            x=center_x - 100,
            y=start_y + spacing + 70,
            width=200,
            height=50,
            text="Redeem",
            callback=self.on_redeem_click,
            font=self.font_normal,
            text_color=(255, 255, 255),
            bg_color=(70, 120, 70),
            hover_color=(100, 150, 100)
        )
        
        # Back button
        self.back_button = Button(
            x=center_x - 220,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=60,
            text="Back",
            callback=self.on_back_click,
            font=self.font_normal,
            text_color=(255, 255, 255),
            bg_color=(70, 70, 120),
            hover_color=(100, 100, 150)
        )
        
        # Exit button
        self.exit_button = Button(
            x=center_x + 20,
            y=SCREEN_HEIGHT - 100,
            width=200,
            height=60,
            text="Exit",
            callback=self.on_exit_click,
            font=self.font_normal,
            text_color=(255, 255, 255),
            bg_color=(120, 70, 70),
            hover_color=(150, 100, 100)
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
        try:
            pygame.mixer.music.set_volume(volume)
        except:
            pass  # Mixer might not be initialized
        
        print(f"Volume adjusted to: {int(value)}%")
    
    def on_redeem_click(self):
        """Callback for Redeem button - process code redemption"""
        code = self.code_input.get_text().strip()
        
        if not code:
            self.show_message("Please enter a code", (255, 200, 0))
            return
        
        # Attempt to redeem the code using CodeManager
        success, message, coins = self.code_manager.redeem_code(code)
        
        if success:
            # Add coins to player
            self.game.player_data.add_coins(coins)
            self.show_message(message, (100, 255, 100))
            self.code_input.clear()
            print(f"Code '{code}' redeemed: +{coins} coins")
        else:
            self.show_message(message, (255, 100, 100))
            self.code_input.clear()
    
    def on_back_click(self):
        """Callback for Back button - return to previous state"""
        print("Back button clicked - returning to previous state")
        # Return to loading or main lobby depending on where we came from
        if hasattr(self.game, 'previous_state') and self.game.previous_state:
            self.game.change_state(self.game.previous_state)
        else:
            self.game.change_state('loading')
    
    def on_exit_click(self):
        """Callback for Exit button - close the game"""
        print("Exit button clicked - closing game")
        self.game.quit()
    
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
        # Delegate to UI components
        if self.sound_slider:
            self.sound_slider.handle_event(event)
        if self.code_input:
            self.code_input.handle_event(event)
        if self.redeem_button:
            self.redeem_button.handle_event(event)
        if self.back_button:
            self.back_button.handle_event(event)
        if self.exit_button:
            self.exit_button.handle_event(event)
    
    def update(self, dt):
        """
        Update game state logic
        
        Args:
            dt: Delta time in seconds since last update
        """
        # Update UI components
        if self.sound_slider:
            self.sound_slider.update()
        if self.code_input:
            self.code_input.update(dt)
        if self.redeem_button:
            self.redeem_button.update(dt)
        if self.back_button:
            self.back_button.update(dt)
        if self.exit_button:
            self.exit_button.update(dt)
        
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
        
        # Draw title
        if self.font_title:
            title_surface = self.font_title.render("Settings", True, (255, 255, 255))
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(title_surface, title_rect)
        
        # Draw sound label
        if self.font_normal:
            sound_label = self.font_normal.render("Volume Control", True, (255, 255, 255))
            sound_rect = sound_label.get_rect(center=(SCREEN_WIDTH // 2, 170))
            screen.blit(sound_label, sound_rect)
        
        # Draw code redemption label
        if self.font_normal:
            code_label = self.font_normal.render("Code Redemption", True, (255, 255, 255))
            code_rect = code_label.get_rect(center=(SCREEN_WIDTH // 2, 270))
            screen.blit(code_label, code_rect)
        
        # Draw UI components
        if self.sound_slider:
            self.sound_slider.draw(screen)
        if self.code_input:
            self.code_input.draw(screen)
        if self.redeem_button:
            self.redeem_button.draw(screen)
        if self.back_button:
            self.back_button.draw(screen)
        if self.exit_button:
            self.exit_button.draw(screen)
        
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