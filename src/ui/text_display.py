import pygame
from typing import Callable
from src.utils.constants import PATH_FONTS, COLOR_WHITE, COLOR_BLACK, COLOR_PURPLE, COLOR_YELLOW

class TextDisplay:
    def __init__(
            self, 
            x: int,
            y: int,
            text: str,
            color: tuple[int, int, int] = COLOR_WHITE,
            size: int = 32,
            enable: bool = True
    ):

        self.text = text

        if self.text:
            self.font = pygame.font.Font(PATH_FONTS + 'Monocraft.ttf', size)
            self.color = color
            self.textSurface = self.font.render(self.text, True, self.color)
            self.textRect = self.textSurface.get_rect(centerx = x, centery = y)
                  
        self.enable = enable


    def render(self, screen: pygame.Surface) -> None:
        if not self.enable:
            return
        screen.blit(self.textSurface, self.textRect)

    def setEnable(self, enable: bool):
        self.enable = enable