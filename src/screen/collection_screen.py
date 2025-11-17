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
                y= 100,
                text= 'NAME1',
                size= 18,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x + 180,
                y= 100,
                text= 'NAME2',
                size= 18,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x - 180,
                y= 500,
                text= 'STATE1',
                size= 14,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x + 180,
                y= 500,
                text= 'STATE2',
                size= 14,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x - 180,
                y= 530,
                text= 'TOTAL1',
                size= 14,
                color= COLOR_BLACK
            ),
            TextDisplay(
                x= self.center_x + 180,
                y= 530,
                text= 'TOTAL2',
                size= 14,
                color= COLOR_BLACK
            )


        ]

        self.images = [
            Image(
                x= self.center_x - 180,
                y= self.center_y - 55,
                image_name= 'hero1.png',
                path_prefix= PATH_PORTRAITS,
                scale= 0.45
            ),
            Image(
                x= self.center_x + 180,
                y= self.center_y - 55,
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
        self.page -= 1
        self.update_page()

    def forward(self):
        self.page += 1
        self.update_page()

    def update_page(self):
        last_page = (len(CHARACTER) + 1) // 2
        self.page = max(1, min(last_page, self.page))

        owned = set(self.manager.player_data.owned_characters)

        start_idx = (self.page - 1) * 2

        for slot in range(2):
            idx = start_idx + slot
            img = self.images[slot]
            character_name = self.textDisplays[slot]
            character_state = self.textDisplays[slot + 2]
            character_totalpower = self.textDisplays[slot + 4]


            if idx < len(CHARACTER):
                img.setEnable(True)
                character_name.setEnable(True)

                img.setImage(f"hero{idx + 1}.png")
                character_name.setText(CHARACTER[idx].name)
                character_state.setText(f'ATK [{CHARACTER[idx].atk}] | DEF [{CHARACTER[idx].defense}]')
                character_totalpower.setText(f'TOTAL POWER [{CHARACTER[idx].totalPower}]')


                if (idx + 1) not in owned:
                    img.makeGray()
                    character_name.setText('???')
                    character_state.setText(f'ATK [???] | DEF [???]')
                    character_totalpower.setText(f'TOTAL POWER [???]')
                else:
                    if hasattr(img, "resetColor"):
                        img.resetColor()
            else:
                img.setEnable(False)
                character_name.setEnable(False)
