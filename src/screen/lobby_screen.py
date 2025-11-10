import pygame
from src.screen.base_screen import BaseScreen
from src.utils.constants import PATH_BACKGROUNDS
from src.ui.button import Button

class LobbyScreen(BaseScreen):
    def __init__(self):
        self.setBackground(PATH_BACKGROUNDS + 'town1.png')
        self.buttons: list[Button] = []

        self._setup_ui()

    def _setup_ui(self) -> None:
        self.buttons = [
            Button(
                x= 1100,
                y= 100,
                image_name='wood1_background.png',
                text= 'test',
                callback= self.test,
                font_size= 36
            )
        ]

    def render(self, screen):
        screen.blit(self.background, (0,0))

        for button in self.buttons:
            button.render(screen)

    def handleEvents(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            for button in self.buttons:
                button.handleEvent(event)

    def test(self):
        print('test')
