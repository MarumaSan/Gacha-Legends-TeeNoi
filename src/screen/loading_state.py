import pygame
from src.core.game_state import GameState
from src.utils import assets
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT
from src.ui.image_button import _ImageButton
from src.ui.text_display import TextDisplay
from src.utils import player

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game import Game


class LoadingState(GameState):
    """Loading screen state with player selection (PLAYER 1, PLAYER 2, QUIT)"""
    def __init__(self, game: 'Game'):
        super().__init__(game)
        self.background = None
        self.font = None

        self.btn_player1 = None
        self.btn_player2 = None
        self.btn_battle = None
        self.btn_quit = None
        self.btn_question = None

        self.BUTTON_BASE_PATH = 'assets/ui/12.png'
        self.BUTTON_SCALE = 1.2

    def enter(self):
        # หยุดเพลงในหน้า loading
        pygame.mixer.music.stop()
        
        try:
            self.background = assets.load_image('assets/backgrounds/town_2.png').convert()
        except Exception as e:
            print(f"Cannot load background: {e}")
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((50, 50, 100))

        self.font = assets.load_font('assets/fonts/Monocraft.ttf', 60)
        self.title_player_select = TextDisplay(
            'Select Player',
            self.font,
            (228, 162, 31),
            centered=True,
            position=(SCREEN_WIDTH // 2, 200)
        )

        try:
            base_img = assets.load_image(self.BUTTON_BASE_PATH).convert_alpha()
            btn_player1 = assets.load_image('assets/ui/player1.png').convert_alpha()
            btn_player2 = assets.load_image('assets/ui/player2.png').convert_alpha()
            img_character1 = assets.load_image('assets/portraits/hero21.png').convert_alpha()
            img_character2 = assets.load_image('assets/portraits/hero17.png').convert_alpha()
            Btn_battle = assets.load_image('assets/ui/battle_button.png').convert_alpha()

        except Exception as e:
            print(f"Error: {e}")

        centers = [
            (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 40),
            (SCREEN_WIDTH // 2 + 70, SCREEN_HEIGHT // 2 - 40),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80),
            (SCREEN_WIDTH // 2, 680),
            (200, SCREEN_HEIGHT // 2),
            (1080, SCREEN_HEIGHT // 2)
        ]

        self.btn_player1 = _ImageButton(
            btn_player1, 
            centers[0], 
            on_click=self.on_player1_click,
            scale=0.8, 
            use_mask=True, 
        )
        self.btn_player2 = _ImageButton(
            btn_player2, 
            centers[1], 
            on_click=self.on_player2_click,
            scale=0.8, 
            use_mask=True, 
        )
        self.btn_battle = _ImageButton(
            Btn_battle, 
            centers[2], 
            on_click=self.on_battle_click,
            scale=0.8, 
            use_mask=True,
        )
        # self.btn_quit = _ImageButton(
        #     base_img, 
        #     centers[3], 
        #     on_click=self.on_exit_click,
        #     scale=self.BUTTON_SCALE, 
        #     use_mask=True, 
        #     text="QUIT", 
        #     font=self.font
        # )

        self.img_character1 = _ImageButton(
            img_character1,
            centers[4],
            scale=0.5,
            use_mask=True
        )

        self.img_character2 = _ImageButton(
            img_character2,
            centers[5],
            scale=0.5,
            use_mask=True
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
        self.btn_question = _ImageButton(
            question_img,
            center=(SCREEN_WIDTH - 40, 40),
            on_click=self.on_question_click,
            scale=1.0,
            use_mask=False
        )

    def on_player1_click(self):
        if getattr(self.game.state_manager, "transitioning", False):
            return
        print("Select PLAYER 1")
        # โหลดข้อมูลผู้เล่น 1
        self.game.load_player_data(1)
        # เข้าเกม
        if hasattr(self.game, "change_state_then_fade_in"):
            self.game.change_state_then_fade_in('main_lobby', duration=0.6)
        else:
            self.game.change_state('main_lobby')

    def on_player2_click(self):
        if getattr(self.game.state_manager, "transitioning", False):
            return
        print("Select PLAYER 2")
        # โหลดข้อมูลผู้เล่น 2
        self.game.load_player_data(2)
        # เข้าเกม
        if hasattr(self.game, "change_state_then_fade_in"):
            self.game.change_state_then_fade_in('main_lobby', duration=0.6)
        else:
            self.game.change_state('main_lobby')

    def on_battle_click(self):
        player1 = player.load_player_data(1)
        player2 = player.load_player_data(2)
        if len(player1['owned_heroes']) <= 5 and len(player2['owned_heroes']) <= 5:
            print('Players must have 5 characters each.')
        elif player1['coins'] <= 0 or player2['coins'] <= 0:
            print('Money 0 cannot play')
        else:
            if getattr(self.game.state_manager, "transitioning", False):
                return
            if hasattr(self.game, "change_state_then_fade_in"):
                self.game.change_state_then_fade_in('battle', duration=0.6)
            else:
                self.game.change_state('battle')
        
            
        
    
    # def on_exit_click(self):
    #     if getattr(self.game.state_manager, "transitioning", False):
    #         return
    #     print("คลิกปุ่มออกเกม")
    #     self.game.quit()
    
    def on_question_click(self):
        if getattr(self.game.state_manager, "transitioning", False):
            return
        self.game.change_state('how_to_play')

    def handle_event(self, event):
        if getattr(self.game.state_manager, "transitioning", False):
            return
        if self.btn_player1: self.btn_player1.handle_event(event)
        if self.btn_player2: self.btn_player2.handle_event(event)
        if self.btn_battle: self.btn_battle.handle_event(event)
        # if self.btn_quit: self.btn_quit.handle_event(event)
        if self.btn_question: self.btn_question.handle_event(event)

    def update(self, dt):
        if getattr(self.game.state_manager, "transitioning", False):
            return
        if self.btn_player1: self.btn_player1.update(dt)
        if self.btn_player2: self.btn_player2.update(dt)
        if self.btn_battle: self.btn_battle.update(dt)
        if self.btn_quit: self.btn_quit.update(dt)
        if self.btn_question: self.btn_question.update(dt)

    def draw(self, screen: pygame.Surface):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((30, 30, 60))
        if self.title_player_select: self.title_player_select.draw(screen)
        if self.btn_player1: self.btn_player1.draw(screen)
        if self.btn_player2: self.btn_player2.draw(screen)
        if self.btn_battle: self.btn_battle.draw(screen)
        # if self.btn_quit: self.btn_quit.draw(screen)
        if self.btn_question: self.btn_question.draw(screen)
        if self.img_character1: self.img_character1.draw(screen)
        if self.img_character2: self.img_character2.draw(screen)

    def exit(self):
        pass
