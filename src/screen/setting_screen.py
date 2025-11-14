import pygame
from src.screen.base_screen import BaseScreen
from src.ui.text_display import TextDisplay
from src.ui.button import Button
from src.utils.constants import *

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game_manager import GameManager

class SettingScreen(BaseScreen):
    def __init__(self, manager: 'GameManager'):
        super().__init__(manager)
        self.setBackground('town2.png')

        self.bg_rect = self.background.get_rect()
        self.center_x, self.center_y = self.bg_rect.center

        self.dragging = False

        self._setup_ui()
    
    def _setup_ui(self):
        self.sliderButton_x = 640
        self.sliderButton_y = 350

        self.sliderBar = Button(
                x= self.center_x,
                y= 350,
                image_name= 'slider_bar.png'
        )
        self.sliderButton = Button(
                x= self.sliderButton_x,
                y= self.sliderButton_y,
                image_name= 'slider_button.png'
        )

        self.textDisplay = TextDisplay(
            x= self.center_x,
            y= 200,
            text= 'SETTING',
            size= 60
        )

        self.saveButton = Button(
            x= self.center_x,
            y= 660,
            image_name= 'save_button.png',
            callback= self._backToLobby
        )

        self.button = Button(
                x= self.center_x,
                y= 470,
                image_name= 'wood1_background.png',
                font_size= 16,
                text= 'Logout',
                text_color= COLOR_YELLOW,
                callback= self._backToLoad
            )

    def handleEvents(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            self.saveButton.handleEvent(event)

            self.button.handleEvent(event)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.sliderButton.imageRect.collidepoint(event.pos):
                    self.dragging = True

            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

            if event.type == pygame.MOUSEMOTION and self.dragging:
                mouse_x, mouse_y = event.pos

                new_x = mouse_x - self.sliderButton.imageRect.width // 2

                new_x = max(610, min(new_x, 750))

                self.sliderButton.imageRect.x = new_x

                slider_value = (new_x - 610) / (750 - 610)
                print(f"value: {slider_value:.2f}")

    def render(self, screen):
        screen.blit(self.background, (0,0))

        self.textDisplay.render(screen)
        self.sliderBar.render(screen)
        self.sliderButton.render(screen)
        self.saveButton.render(screen)
        
        self.button.render(screen)
    
    def _backToLobby(self):
        self.manager.screenManager.changeScreen('lobby')

    def _backToLoad(self):
        self.manager.screenManager.changeScreen('load')
