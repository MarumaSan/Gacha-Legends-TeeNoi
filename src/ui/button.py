import pygame
from typing import Callable
from src.utils.constants import PATH_UI, PATH_FONTS, COLOR_WHITE, COLOR_BLACK, COLOR_PURPLE, COLOR_YELLOW

class Button:
    def __init__(
            self, 
            x: int,
            y: int,
            image_name: str,
            text: str = None,
            text_color: str = COLOR_WHITE,
            text_x: int = None,
            text_y: int = None,
            font_size: int = 32,
            callback: Callable = None,
            enable: bool = True
    ):

        self.image = pygame.image.load(PATH_UI + image_name).convert_alpha()
        self.imageRect = self.image.get_rect(center=(x, y))

        self.text = text
        self.callback = callback

        if self.text:
            self.font = pygame.font.Font(PATH_FONTS + 'Monocraft.ttf', font_size)
            self.color = text_color
            self.textSurface = self.font.render(self.text, True, self.color)
            if text_x and text_y:
                self.textRect = self.textSurface.get_rect(centerx = text_x, centery = text_y)
            elif text_x:
                self.textRect = self.textSurface.get_rect(centerx = text_x, centery=self.imageRect.centery)
            elif text_y:
                self.textRect = self.textSurface.get_rect(centerx=self.imageRect.centerx, centery = text_y)
            else :
                self.textRect = self.textSurface.get_rect(center=self.imageRect.center)
                
        self.enable = enable

    def handleEvent(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.enable:
            if self.imageRect.collidepoint(event.pos):
                if callable(self.callback):
                    self.callback()

    def render(self, screen: pygame.Surface) -> None:
        if self.enable:
            screen.blit(self.image, self.imageRect)

            if self.text:
                screen.blit(self.textSurface, self.textRect)

    def setEnable(self, enable: bool):
        self.enable = enable