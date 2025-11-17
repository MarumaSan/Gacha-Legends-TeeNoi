import pygame
from src.ui.button import Button
from src.ui.text_display import TextDisplay
from src.ui.image import Image
from src.screen.base_screen import BaseScreen

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

        self._setup_ui()

    def _setup_ui(self) -> None:
        pass

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

    def start_screen(self):
        pass