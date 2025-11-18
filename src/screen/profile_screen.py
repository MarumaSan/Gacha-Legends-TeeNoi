import pygame
from src.ui.button import Button
from src.ui.text_display import TextDisplay
from src.ui.image import Image
from src.screen.base_screen import BaseScreen
from src.utils.constants import COLOR_BLACK, CHARACTER

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game_manager import GameManager

class ProfileScreen(BaseScreen):
    def __init__(self, manager: 'GameManager'):
        super().__init__(manager)

        self.setBackground('book.png')

        self.buttons: list[Button] = []
        self.textDisplays: list[TextDisplay] = []
        self.images: list[Image] = []

        self._setup_ui()

    def _setup_ui(self) -> None:
        self.textDisplays = [
            TextDisplay(
                x= self.center_x - 180,
                y= 150,
                text= 'STATISTICS',
                size= 25,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x - 180,
                y= 245,
                text= 'TOTAL POWER',
                size= 18,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x - 180,
                y= 280,
                text= '0',
                size= 16,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x - 180,
                y= 340,
                text= 'COLLECTED',
                size= 18,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x - 180,
                y= 375,
                text= '0',
                size= 16,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x - 180,
                y= 435,
                text= 'ALL GOLD',
                size= 18,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x - 180,
                y= 470,
                text= '0',
                size= 16,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x + 190,
                y= 150,
                text= 'LEADERBOARD',
                size= 25,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x + 110,
                y= 245,
                text= 'NAME',
                size= 18,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x + 110,
                y= 280,
                text= 'NAME',
                size= 16,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x + 110,
                y= 315,
                text= 'NAME',
                size= 16,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x + 270,
                y= 245,
                text= 'POWER',
                size= 18,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x + 270,
                y= 280,
                text= 'POWER',
                size= 16,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x + 270,
                y= 315,
                text= 'POWER',
                size= 16,
                color= COLOR_BLACK
            )

        ]

        self.buttons = [
            Button(
                x= self.center_x,
                y= 660,
                image_name= 'wood1_background.png',
                text= 'RETURN TO LOBBY',
                font_size= 14,
                callback= self.backToLobby
            )
        ]

    def render(self, screen):
        screen.blit(self.background, (0,0))

        for button in self.buttons:
            button.render(screen)

        for text in self.textDisplays:
            text.render(screen)

        for image in self.images:
            image.render(screen)

        self.textDisplays[2].setText(f'{self.manager.helpers.get_total_power(self.manager.current_player_id)}')
        self.textDisplays[4].setText(f'{len(self.manager.player_data.owned_characters)} / {len(CHARACTER)}')
        self.textDisplays[6].setText(f'{self.manager.player_data.coins}')
        self.textDisplays[9].setText(f'{self.leaderboard[0]['name']}')
        self.textDisplays[10].setText(f'{self.leaderboard[1]['name']}')
        self.textDisplays[12].setText(f'{self.leaderboard[0]['power']}')
        self.textDisplays[13].setText(f'{self.leaderboard[1]['power']}')

        self.update_transition(screen)
    
    def update(self):
        pass

    def handleEvents(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if self._dispatch_event(self.buttons, event):
                continue

    def backToLobby(self):
        self.manager.screenManager.changeScreen('lobby')
    
    def start_screen(self):
        another_player = 'player1' if self.manager.current_player_id != 'player1' else 'player2'
        another_player_name = 'PLAYER 1' if self.manager.current_player_id != 'player1' else 'PLAYER 2'
        players = [
            {"name": "ME", "power": self.manager.helpers.get_total_power(self.manager.current_player_id)},
            {"name": another_player_name, "power": self.manager.helpers.get_total_power(another_player)}
        ]
        self.leaderboard = sorted(players, key=lambda x: x["power"], reverse=True)