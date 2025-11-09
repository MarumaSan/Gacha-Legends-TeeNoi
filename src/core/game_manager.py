import pygame
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PATH_UI
from src.screen.lobby_screen import LobbyScreen

class GameManager:
    def __init__(self):
        pygame.init()

        self.logo = pygame.image.load(PATH_UI + 'logo.png')

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Gacha Legends')
        pygame.display.set_icon(self.logo)

        self.clock = pygame.time.Clock()
        
        self.running = False

        self.currentScreen = LobbyScreen()

    def run(self):
        self.running = True
        
        while self.running:
            events = pygame.event.get()
        
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.render()

            pygame.display.flip()

            self.clock.tick(FPS)
    
    def render(self) -> None:
        currentScreen = self.currentScreen
        if currentScreen:
            currentScreen.render(self.screen)