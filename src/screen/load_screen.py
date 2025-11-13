import pygame
from src.screen.base_screen import BaseScreen
from src.ui.image import Image
from src.utils.constants import PATH_PORTRAITS

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game_manager import GameManager

class LoadScreen(BaseScreen):
    def __init__(self, manager: 'GameManager'):
        super().__init__(manager)
        self.setBackground('town2.png')
        self.images: list[Image] = []
        self._setup_ui()
    
    def _setup_ui(self):
        self.images = [
            Image(
                x= 200,
                y= 360,
                image_name= 'hero21.png',
                path_prefix= PATH_PORTRAITS,
                scale= 0.5
            ),
            Image(
                x= 1080,
                y= 360,
                image_name= 'hero17.png',
                path_prefix= PATH_PORTRAITS,
                scale= 0.5
            )
        ]
    
    def render(self, screen):
        screen.blit(self.background, (0,0))

        for image in self.images:
            image.render(screen)

    def handleEvents(self, events):
        for event in events:
            pass
    
    def update(self):
        pass
