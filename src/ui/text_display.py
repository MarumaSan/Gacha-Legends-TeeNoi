import pygame
from src.utils.constants import PATH_FONTS, COLOR_WHITE

class TextDisplay:
    def __init__(
            self, 
            x: int,
            y: int,
            text: str,
            font_size: int = 32,
            enable: bool = True
    ):
        self.x = x
        self.y = y

        self.text = text
        self.font = pygame.font.Font(PATH_FONTS + 'Monocraft.ttf', font_size)
        self.color = COLOR_WHITE

        self.enable = enable

    def render(self, screen: pygame.Surface) -> None:
        if self.enable:
            textSurface = self.font.render(self.text, True, self.color)
            screen.blit(textSurface, (self.x, self.y))

    def setEnable(self, enable: bool):
        self.enable = enable