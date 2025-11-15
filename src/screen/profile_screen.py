import pygame
from src.ui.button import Button
from src.ui.text_display import TextDisplay
from src.ui.image import Image
from src.screen.base_screen import BaseScreen
from src.utils.constants import COLOR_BLACK, CHARACTER

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game_manager import GameManager

CHARACTER_BY_ID = {char.id: char for char in CHARACTER}


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
                x= self.center_x + 270,
                y= 245,
                text= 'POWER',
                size= 18,
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

        self.textDisplays[2].setText(f'{self.get_total_power()}')
        self.textDisplays[4].setText(f'{len(self.manager.player_data.owned_characters)} / {len(CHARACTER)}')
        self.textDisplays[6].setText(f'{self.manager.player_data.coins}')

        self.update_transition(screen)
    
    def update(self):
        pass

    def handleEvents(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            for button in self.buttons:
                button.handleEvent(event)

    def backToLobby(self):
        self.manager.screenManager.changeScreen('lobby')
    
    def on_enter(self):
        self.transitioning = True
        self.fade_alpha = 255
        
    def get_total_power(self):
        total = 0
        for hero_id in self.manager.player_data.owned_characters:
            hero = CHARACTER_BY_ID.get(hero_id)
            if hero:
                total += hero.totalPower
        return total
