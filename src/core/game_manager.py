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
        
        self.currentScreen = LobbyScreen(self)

    def run(self):
        self.running = True
        
        while self.running:
            self.handleEvents()

            self.render()

            pygame.display.flip()

            self.clock.tick(FPS)
    
    def render(self) -> None:
        self.currentScreen.render(self.screen)
    
    def handleEvents(self) -> None:
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        
        self.currentScreen.handleEvents(events)
    
    def changeScreen(self, new_screen):
        self.currentScreen = new_screen