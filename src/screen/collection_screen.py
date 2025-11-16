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

        # self.image_list = [f'hero{i + 1}.png' for i in range(len(CHARACTER))]

    def backward(self):
        self.update_page(-1)

    def forward(self):
        self.update_page(1)

    def update_page(self, c):
        if len(CHARACTER) % 2 == 0:
            if 1 <= self.page < floor(len(CHARACTER) / 2):
                self.page += c

                image1 = f'hero{(2 * self.page) - 1}.png'
                image2 = f'hero{(2 * self.page)}.png'

                self.images[0].setImage(image1)
                self.images[1].setImage(image2)
        else:
            if 1 <= self.page < floor(len(CHARACTER) / 2):
                self.page += c

                image1 = f'hero{(2 * self.page) - 1}.png'
                image2 = f'hero{(2 * self.page)}.png'

                self.images[0].setImage(image1)
                self.images[1].setImage(image2)
            
            if self.page == floor(len(CHARACTER) / 2):
                self.page += 1

                image1 = f'hero{(2 * self.page) - 1}.png'
                image2 = f'hero{(2 * self.page)}.png'

                self.images[0].setImage(image1)
                self.images[1].setEnable(False)
                self.textDisplays[1].setEnable(False)


        
    def get_total_power(self, Player: str):
        total = 0
        for hero_id in self.manager.getPlayerData(Player).owned_characters:
            hero = CHARACTER_BY_ID.get(hero_id)
            if hero:
                total += hero.totalPower
        return total