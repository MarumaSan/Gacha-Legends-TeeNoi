import pygame
from typing import Optional, Callable

class LoadImage:
    def __init__(
        self,
        x: int,
        y: int,
        path: str,
        enable: bool = True,
        width: int | None = None,
        height: int | None = None,
        scale: float = 1.0,
        callback: Optional[Callable] = None
    ):
        self.x = x
        self.y = y

        self.path = path
        self.enable = enable
        self.callback = callback

        self._width = width
        self._height = height
        self._scale = scale

        self.base_image: pygame.Surface = pygame.image.load(self.path).convert_alpha()

        self.image: pygame.Surface = self._build_image()
        self._original_image: pygame.Surface = self.image.copy()

        self.imageRect: pygame.Rect = self.image.get_rect(center=(x, y))

    def _build_image(self) -> pygame.Surface:
        if self._width is not None and self._height is not None:
            return pygame.transform.smoothscale(
                self.base_image, (self._width, self._height)
            )

        if self._scale != 1.0:
            bw, bh = self.base_image.get_size()
            new_w = int(bw * self._scale)
            new_h = int(bh * self._scale)
            return pygame.transform.smoothscale(self.base_image, (new_w, new_h))

        return self.base_image.copy()

    def render(self, screen: pygame.Surface) -> None:
        if self.enable:
            screen.blit(self.image, self.imageRect)

    def setScale(self, scale: float) -> None:
        self._scale = scale
        self.image = self._build_image()
        self._original_image = self.image.copy()
        self.imageRect = self.image.get_rect(center=self.imageRect.center)

    def setEnable(self, enable: bool) -> None:
        self.enable = enable

    def setPos(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.imageRect.center = (x, y)

    def setImage(self, path: str):
        self.base_image: pygame.Surface = pygame.image.load(path).convert_alpha()

        self.image: pygame.Surface = self._build_image()
        self._original_image: pygame.Surface = self.image.copy()

        self.imageRect: pygame.Rect = self.image.get_rect(center=(self.x, self.y))

    def handleEvent(self, event: pygame.event.Event) -> bool:
        if not self.enable:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.imageRect.collidepoint(event.pos):
                if callable(self.callback):
                    self.callback()
                    return True
                return False
        return False
