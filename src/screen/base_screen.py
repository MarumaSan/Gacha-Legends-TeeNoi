import pygame
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class BaseScreen:
    def handleEvents(self, events: list[pygame.event.Event]) -> None:
        pass
    
    def _setup_ui(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        pass

    def update(self) -> None:
        pass

    def setBackground(self, background_path: str) -> None:
        self.background_path = background_path
        self.background = pygame.image.load(background_path).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))