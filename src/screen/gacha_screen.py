import pygame
from src.ui.button import Button
from src.ui.text_display import TextDisplay
from src.ui.image import Image
from src.screen.base_screen import BaseScreen
from src.model.gacha_config import mystic_chest, celestial_chest
from src.utils.constants import COLOR_YELLOW, COLOR_PURPLE

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game_manager import GameManager

class GachaScreen(BaseScreen):
    def __init__(self, manager: 'GameManager'):
        super().__init__(manager)

        self.setBackground('summon2.png')

        self.buttons: list[Button] = []
        self.textDisplays: list[TextDisplay] = []
        self.images: list[Image] = []

        self.chest = mystic_chest
        self.chest_text_color = COLOR_YELLOW

        self._setup_ui()

    def _setup_ui(self) -> None:
        self.textDisplays = [
            TextDisplay(
                x= self.center_x,
                y= 210,
                text= 'CHEST NAME',
                size= 80,
                color= self.chest_text_color,
                callback= self.returnToLobby
            ),
            TextDisplay(
                x= self.center_x,
                y= 600,
                text= 'Return to Lobby',
                size= 16,
                callback= self.returnToLobby
            ),
            TextDisplay(
                x= self.center_x - 120,
                y= self.center_y - 40,
                text= 'coin',
                size= 16,
                callback= self.returnToLobby,
                color= COLOR_YELLOW
            ),
            TextDisplay(
                x= self.center_x + 120,
                y= self.center_y - 40,
                text= 'coin',
                size= 16,
                callback= self.returnToLobby,
                color= COLOR_YELLOW
            ),
            TextDisplay(
                x= self.center_x,
                y= self.center_y + 100,
                text= 'back',
                size= 16,
                callback= self.openLayout1,
                enable= False
            ),
            TextDisplay(
                x= self.center_x,
                y= self.center_y,
                text= 'drop rate',
                size= 16,
                enable= False
            )
        ]

        self.buttons = [
            Button(
                x= self.center_x - 120,
                y= self.center_y + 50,
                image_name= self.chest.chest_type + '_chest_background.png',
                font_size= 11,
                text= 'SUMMON X1',
                text_y= self.center_y + 98
            ),
            Button(
                x= self.center_x + 120,
                y= self.center_y + 50,
                image_name= self.chest.chest_type + '_chest_background.png',
                font_size= 11,
                text= 'SUMMON X10',
                text_y= self.center_y + 98
            ),
            Button(
                x= 1240,
                y= 40,
                image_name= 'mark.png',
                callback= self.mark
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

            for text in self.textDisplays:
                text.handleEvent(event)

    def start_screen(self):
        self.chest = mystic_chest if self.manager.chest_type == 'mystic' else celestial_chest

        chest_text_color = COLOR_YELLOW if self.chest.chest_type == 'mystic' else COLOR_PURPLE

        self.textDisplays[0].setText(self.chest.chest_name)
        self.textDisplays[0].setColor(chest_text_color)

        for i in range(2):
            self.buttons[i].setImage(f'{self.chest.chest_path}')

        self.textDisplays[2].setText(f'{self.chest.cost} COINS')
        self.textDisplays[3].setText(f'{self.chest.cost * 10} COINS')

    def returnToLobby(self):
        self.manager.screenManager.changeScreen('lobby')

    def mark(self):
        self.closeLayout1()
        self.textDisplays[4].setEnable(True)
        self.textDisplays[5].setEnable(True)
        self.textDisplays[5].setText(f'Rare : {self.chest.drop_rates['rare']} | Epic : {self.chest.drop_rates['epic']} | Legendary : {self.chest.drop_rates['legendary']} | Extreme : {self.chest.drop_rates['extreme']}')
        


    def closeLayout1(self):
        for i in range(4): self.textDisplays[i].setEnable(False)
        for i in range(3): self.buttons[i].setEnable(False)

    def openLayout1(self):
        for text in self.textDisplays:
            text.setEnable(False)

        for image in self.images:
            image.setEnable(False)

        for i in range(4): self.textDisplays[i].setEnable(True)
        for i in range(3): self.buttons[i].setEnable(True)
