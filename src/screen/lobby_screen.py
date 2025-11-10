import pygame
from src.screen.base_screen import BaseScreen
from src.ui.button import Button
from src.ui.text_display import TextDisplay

class LobbyScreen(BaseScreen):
    def __init__(self):
        self.setBackground('town1.png')
        self.buttons: list[Button] = []

        self._setup_ui()

    def _setup_ui(self) -> None:
        self.buttons = [
            Button(
                x= 640,
                y= 50,
                image_name='status_background.png',
                text= 'test',
                font_size= 18
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
