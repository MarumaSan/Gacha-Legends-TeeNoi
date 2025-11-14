import pygame
from src.utils.constants import PATH_PORTRAITS, COLOR_YELLOW
from src.ui.button import Button
from src.ui.text_display import TextDisplay
from src.ui.image import Image
from src.screen.base_screen import BaseScreen

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game_manager import GameManager

class LoadScreen(BaseScreen):
    def __init__(self, manager: 'GameManager'):
        super().__init__(manager)

        self.setBackground('town2.png')

        self.buttons: list[Button] = []
        self.textDisplays: list[TextDisplay] = []
        self.images: list[Image] = []

        self._setup_ui()

        self.animating = False
        self.animation_speed = 10
    
    def _setup_ui(self):
        self.images = [
            Image(
                x= self.center_x - 350,
                y= self.center_y,
                image_name= 'hero21.png',
                path_prefix= PATH_PORTRAITS,
                scale= 0.5,
                target= (200, 0)
            ),
            Image(
                x= self.center_x + 350,
                y= self.center_y,
                image_name= 'hero17.png',
                path_prefix= PATH_PORTRAITS,
                scale= 0.5,
                target= (1080, 0)
            )
        ]

        self.textDisplays = [
            TextDisplay(
                x= self.center_x,
                y= self.center_y - 50,
                text= 'Gacha Legends',
                size= 60
            ),
            TextDisplay(
                x= self.center_x,
                y= self.center_y,
                text= 'Press To Continue',
                size= 15
            ),
            TextDisplay(
                x= self.center_x,
                y= self.center_y - 100,
                text= 'Select Player',
                size= 60,
                enable= False
            )
        ]

        self.buttons = [
            Button(
                x= self.center_x - 125,
                y= self.center_y,
                image_name= 'wood1_background.png',
                text= 'player 1',
                font_size= 16,
                text_color = COLOR_YELLOW,
                enable= False,
                callback= self.player1
            ),
            Button(
                x= self.center_x + 125,
                y= self.center_y,
                image_name= 'wood1_background.png',
                text= 'player 2',
                font_size= 16,
                text_color = COLOR_YELLOW,
                enable= False,
                callback= self.player2
            )
        ]
    
    def render(self, screen):
        screen.blit(self.background, (0,0))

        for image in self.images:
            image.render(screen)

        for text in self.textDisplays:
            text.render(screen)

        for button in self.buttons:
            button.render(screen)

        self.update_transition(screen)

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.backgroundRect.collidepoint(event.pos):
                    self.animating = True
                    self.textDisplays[0].setEnable(False)
                    self.textDisplays[1].setEnable(False)
                    self.textDisplays[2].setEnable(True)
                    self.buttons[0].setEnable(True)
                    self.buttons[1].setEnable(True)
            
            for button in self.buttons:
                if self.images[0].imageRect.centerx == self.images[0].target[0]:
                    button.handleEvent(event)
    
    def update(self):
        if self.animating:

            done_count = 0

            for image in self.images:
                if image.target[0] is None:
                    done_count += 1
                    continue

                cx = image.imageRect.centerx
                tx = image.target[0]

                if cx == tx:
                    done_count += 1
                    continue

                if cx < tx:
                    cx = min(cx + self.animation_speed, tx)
                else:
                    cx = max(cx - self.animation_speed, tx)

                image.imageRect.centerx = cx

            if done_count == len(self.images):
                self.animating = False

    def player1(self):
        self.manager.selectPlayer('player1')
        self.manager.screenManager.changeScreen('lobby')
        pygame.mixer.music.set_volume(self.manager.player_data.setting['volume'])

    def player2(self):
        self.manager.selectPlayer('player2')
        self.manager.screenManager.changeScreen('lobby')
        pygame.mixer.music.set_volume(self.manager.player_data.setting['volume'])
