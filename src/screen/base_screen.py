import pygame
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, PATH_BACKGROUNDS

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game_manager import GameManager

class BaseScreen:
    def __init__(self, manager: 'GameManager'):
        self.manager = manager

        self.transitioning = True
        self.fade_alpha = 255
        self.fade_speed = 7

        self.screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.fade_surface = pygame.Surface(self.screen_size).convert_alpha()
        self.fade_surface.fill((0, 0, 0))

    def handleEvents(self, events: list[pygame.event.Event]) -> None:
        pass
    
    def _setup_ui(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        pass

    def update(self) -> None:
        pass

    def on_enter(self) -> None:
        self.transitioning = True
        self.fade_alpha = 255
    
    def on_exit(self) -> None:
        pass

    def setBackground(self, background_name: str) -> None:
        self.background_path = PATH_BACKGROUNDS + background_name
        self.background = pygame.image.load(self.background_path).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.backgroundRect = self.background.get_rect()
        self.center_x, self.center_y = self.backgroundRect.center

    def update_transition(self, screen: pygame.Surface):
        if self.transitioning:
            self.fade_surface.set_alpha(self.fade_alpha)
            screen.blit(self.fade_surface, (0, 0))

            self.fade_alpha -= self.fade_speed
            if self.fade_alpha <= 0:
                self.fade_alpha = 255
                self.transitioning = False
                self.transition_phase = None