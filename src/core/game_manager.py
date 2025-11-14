import pygame
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PATH_UI
from src.core.screen_manager import ScreenManager
from src.screen.load_screen import LoadScreen
from src.screen.lobby_screen import LobbyScreen
from src.screen.setting_screen import SettingScreen

class GameManager:
    def __init__(self):
        pygame.init()

        self.logo = pygame.image.load(PATH_UI + 'logo.png')

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Gacha Legends')
        pygame.display.set_icon(self.logo)

        self.clock = pygame.time.Clock()
        
        self.running = False
        
        self.screenManager = ScreenManager(self)

        self.loadScreen()

        self.screenManager.changeScreen('lobby')

        self.render()

        self.update()

    def run(self):
        self.running = True
        
        while self.running:
            self.handleEvents()

            self.render()

            pygame.display.flip()

            self.clock.tick(FPS)
    
    def render(self) -> None:
        self.screenManager.currentScreen.render(self.screen)
    
    def handleEvents(self) -> None:
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
        
        self.screenManager.currentScreen.handleEvents(events)

    def update(self) -> None:
        self.screenManager.currentScreen.update()

    def loadScreen(self) -> None:
        self.screenManager.loadScreen('load', LoadScreen(self))
        self.screenManager.loadScreen('lobby', LobbyScreen(self))
        self.screenManager.loadScreen('setting', SettingScreen(self))
        
