import pygame
from typing import Callable
from src.utils.constants import PATH_UI, PATH_FONTS, COLOR_WHITE

class Button:
    def __init__(
            self, 
            x: int,
            y: int,
            image_name: str,
            text: str,
            callback: Callable,
            font_size: int = 32,
    ):

        self.image = pygame.image.load(PATH_UI + image_name).convert_alpha()
        self.imageRect = self.image.get_rect(center=(x, y))

        self.text = text
        self.callback = callback

        self.font = pygame.font.Font(PATH_FONTS + 'Monocraft.ttf', font_size)
        self.color = COLOR_WHITE

    def handleEvent(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.imageRect.collidepoint(event.pos):
                if callable(self.callback):
                    self.callback()

    def render(self, screen: pygame.Surface) -> None:

        screen.blit(self.image, self.imageRect)

        textSurface = self.font.render(self.text, True, self.color)
        textRect = textSurface.get_rect(center=self.imageRect.center)
        screen.blit(textSurface, textRect)