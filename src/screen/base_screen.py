import pygame
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PATH_BACKGROUNDS

class BaseScreen:
    def handleEvents(self, events: list[pygame.event.Event]) -> None:
        pass
    
    def _setup_ui(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        pass

    def update(self) -> None:
        pass

    def setBackground(self, background_name: str) -> None:
        self.background_path = PATH_BACKGROUNDS + background_name
        self.background = pygame.image.load(self.background_path).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))