import pygame
from src.screen.base_screen import BaseScreen
from src.utils.constants import PATH_BACKGROUNDS

class LobbyScreen(BaseScreen):
    def __init__(self):
        self.setBackground(PATH_BACKGROUNDS + 'town1.png')

    def render(self, screen):
        screen.blit(self.background, (0,0))