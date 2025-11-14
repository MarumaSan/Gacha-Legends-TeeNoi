import pygame
from typing import Callable
from src.utils.constants import PATH_UI, PATH_PORTRAITS, PATH_CARDS, PATH_BACKGROUNDS

class Image:
    def __init__(
        self,
        x: int,
        y: int,
        image_name: str,
        path_prefix: str = PATH_UI,
        callback: Callable = None,
        enable: bool = True,
        width: int = None,
        height: int = None,
        scale: float = 1.0,
        target: tuple = None
    ):

        self.target = target

        self.base_image = pygame.image.load(path_prefix + image_name).convert_alpha()

        if width is not None and height is not None:
            self.image = pygame.transform.smoothscale(self.base_image, (width, height))
        elif scale != 1.0:
            bw, bh = self.base_image.get_size()
            new_w = int(bw * scale)
            new_h = int(bh * scale)
            self.image = pygame.transform.smoothscale(self.base_image, (new_w, new_h))
        else:
            self.image = self.base_image.copy()

        self.center = (x, y)
        self.imageRect = self.image.get_rect(center=self.center)

        self.callback = callback
        self.enable = enable

    def handleEvent(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.enable:
            if self.imageRect.collidepoint(event.pos):
                if callable(self.callback):
                    self.callback()

    def render(self, screen: pygame.Surface) -> None:
        if self.enable:
            screen.blit(self.image, self.imageRect)

    def setEnable(self, enable: bool):
        self.enable = enable
