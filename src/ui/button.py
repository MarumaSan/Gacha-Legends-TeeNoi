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
        self.x  = x
        self.y  = y

        self.image = pygame.image.load(PATH_UI + image_name).convert_alpha()
        self.imageRect = self.image.get_rect(center=(x, y))

        self.text = text
        self.callback = callback

        self.font_size = font_size
        self.color = text_color
        self.text_x = text_x
        self.text_y = text_y

        self.font = None
        self.textSurface = None
        self.textRect = None

        if self.text is not None:
            self.font = pygame.font.Font(PATH_FONTS + 'Monocraft.ttf', self.font_size)
            self._update_text_surface()
                
        self.enable = enable

    def handleEvent(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.enable:
            if self.imageRect.collidepoint(event.pos):
                if callable(self.callback):
                    self.callback()

    def render(self, screen: pygame.Surface) -> None:
        if self.enable:
            screen.blit(self.image, self.imageRect)

            if self.textSurface:
                screen.blit(self.textSurface, self.textRect)

    def setEnable(self, enable: bool):
        self.enable = enable

    def setText(self, text: str) -> None:
        self.text = text
        if self.font is None:
            self.font = pygame.font.Font(PATH_FONTS + 'Monocraft.ttf', self.font_size)
        self._update_text_surface()
    
    def setPosition(self, position: tuple[int, int]) -> None:
        self.imageRect.center = position
        if self.text is not None:
            self._update_text_surface()


    def _update_text_surface(self) -> None:
        if self.font is None or self.text is None:
            return

        self.textSurface = self.font.render(self.text, True, self.color)

        if self.text_x and self.text_y:
            self.textRect = self.textSurface.get_rect(centerx=self.text_x, centery=self.text_y)
        elif self.text_x:
            self.textRect = self.textSurface.get_rect(centerx=self.text_x, centery=self.imageRect.centery)
        elif self.text_y:
            self.textRect = self.textSurface.get_rect(centerx=self.imageRect.centerx, centery=self.text_y)
        else:
            self.textRect = self.textSurface.get_rect(center=self.imageRect.center)
        
    def setImage(self, image_name):
        self.image = pygame.image.load(PATH_UI + image_name).convert_alpha()
        self.imageRect = self.image.get_rect(center=(self.x, self.y))
