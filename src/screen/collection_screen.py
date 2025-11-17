import pygame
from math import ceil, floor
from src.ui.button import Button
from src.ui.text_display import TextDisplay
from src.ui.image import Image
from src.screen.base_screen import BaseScreen
from src.utils.constants import COLOR_BLACK, CHARACTER, PATH_PORTRAITS

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game_manager import GameManager

CHARACTER_BY_ID = {char.id: char for char in CHARACTER}


class Collection(BaseScreen):
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
                y= 500,
                text= 'NAME',
                size= 18,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x + 180,
                y= 500,
                text= 'NAME',
                size= 18,
                color= COLOR_BLACK
            )

        ]

        self.images = [
            Image(
                x= self.center_x - 180,
                y= self.center_y - 70,
                image_name= 'hero1.png',
                path_prefix= PATH_PORTRAITS,
                scale= 0.45
            ),
            Image(
                x= self.center_x + 180,
                y= self.center_y - 70,
                image_name= 'hero2.png',
                path_prefix= PATH_PORTRAITS,
                scale= 0.45
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
            ),
            Button(
                x= 100,
                y= self.center_y,
                image_name= 'backward_button.png',
                callback= self.backward
            ),
            Button(
                x= 1180,
                y= self.center_y,
                image_name= 'forward_button.png',
                callback= self.forward
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

        self.update_transition(screen)
    
    def update(self):
        pass

    def handleEvents(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            for button in self.buttons:
                button.handleEvent(event)

    def backToLobby(self):
        self.manager.screenManager.changeScreen('lobby')
    
    def start_screen(self):
        self.page = 1

        self.update_page()

    def backward(self):
        if self.page == ceil(len(CHARACTER) / 2):
            self.images[1].setEnable(True)
            self.textDisplays[1].setEnable(True)
        self.page -= 1
        self.update_page()

    def forward(self):
        self.page += 1
        self.update_page()

    def update_page(self):
        self.page = max(1, min(ceil(len(CHARACTER) / 2), self.page))

        image1 = f'hero{(2 * self.page) - 1}.png'
        character1_name = f'{CHARACTER[(2 * self.page) - 2].name}'
        self.images[0].setImage(image1)
        self.textDisplays[0].setText(character1_name)

        if self.page != ceil(len(CHARACTER) / 2):
            image2 = f'hero{(2 * self.page)}.png'
            self.images[1].setImage(image2)
            character2_name = f'{CHARACTER[(2 * self.page) - 1].name}'
            self.textDisplays[1].setText(character2_name)
        else:
            self.images[1].setEnable(False)
            self.textDisplays[1].setEnable(False)