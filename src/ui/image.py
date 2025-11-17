import pygame
from typing import Callable, Optional
from src.utils.constants import PATH_UI, PATH_PORTRAITS, PATH_CARDS, PATH_BACKGROUNDS

class Image:
    def __init__(
        self,
        x: int,
        y: int,
        image_name: str,
        path_prefix: str = PATH_UI,
        callback: Optional[Callable] = None,
        enable: bool = True,
        width: int | None = None,
        height: int | None = None,
        scale: float = 1.0,
        target: tuple[int, int] | None = None,
        move_speed: float = 10.0,
    ):
        self.x  = x
        self.y  = y

        self.image_name = image_name
        self.path_prefix = path_prefix

        self.enable = enable
        self.callback = callback

        self._width = width
        self._height = height
        self._scale = scale

        self.target: tuple[int, int] | None = target
        self.move_speed: float = move_speed

        self.base_image: pygame.Surface = pygame.image.load(self.path_prefix + self.image_name).convert_alpha()

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

    def handleEvent(self, event: pygame.event.Event) -> None:
        if not self.enable:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.imageRect.collidepoint(event.pos):
                if callable(self.callback):
                    self.callback()

    def update(self) -> None:
        if not self.enable or self.target is None:
            return

        cx, cy = self.imageRect.center
        tx, ty = self.target

        if (cx, cy) == (tx, ty):
            return

        speed = self.move_speed

        if cx < tx:
            cx = min(cx + speed, tx)
        elif cx > tx:
            cx = max(cx - speed, tx)

        if cy < ty:
            cy = min(cy + speed, ty)
        elif cy > ty:
            cy = max(cy - speed, ty)

        self.imageRect.center = (cx, cy)

    def render(self, screen: pygame.Surface) -> None:
        if self.enable:
            screen.blit(self.image, self.imageRect)

    def setImage(self, image_name: str) -> None:
        self.image_name = image_name

        self.base_image = pygame.image.load(
            self.path_prefix + self.image_name
        ).convert_alpha()

        self.image = self._build_image()
        self._original_image = self.image.copy()

        old_center = self.imageRect.center
        self.imageRect = self.image.get_rect(center=old_center)

    def setTarget(self, x: int, y: int) -> None:
        self.target = (x, y)

    def setEnable(self, enable: bool) -> None:
        self.enable = enable

    def setMoveSpeed(self, speed: float) -> None:
        self.move_speed = speed

    @staticmethod
    def to_grayscale(image: pygame.Surface) -> pygame.Surface:
        grayscale = pygame.Surface(image.get_size(), pygame.SRCALPHA)

        arr = pygame.surfarray.pixels3d(image).copy()
        gray = (0.299 * arr[:, :, 0] + 0.587 * arr[:, :, 1] + 0.114 * arr[:, :, 2]).astype("uint8")

        arr2 = pygame.surfarray.pixels3d(grayscale)
        arr2[:, :, 0] = gray
        arr2[:, :, 1] = gray
        arr2[:, :, 2] = gray

        alpha = pygame.surfarray.pixels_alpha(image)
        pygame.surfarray.pixels_alpha(grayscale)[:, :] = alpha

        return grayscale

    def makeGray(self):
        self.image = Image.to_grayscale(self._original_image)
        self.imageRect = self.image.get_rect(center=self.imageRect.center)

    def resetColor(self):
        self.image = self._original_image.copy()
        self.imageRect = self.image.get_rect(center=self.imageRect.center)

    def setImage(self, image_name: str):
        self.base_image: pygame.Surface = pygame.image.load(self.path_prefix + image_name).convert_alpha()

        self.image: pygame.Surface = self._build_image()
        self._original_image: pygame.Surface = self.image.copy()

        self.imageRect: pygame.Rect = self.image.get_rect(center=(self.x, self.y))