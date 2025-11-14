import pygame
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PATH_UI
from src.model.player_data import PlayerData
from src.core.save_system import SaveSystem
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

        self.save_system = SaveSystem('player1')
        self.player_data = self.load_or_create_player_data()

        self.screenManager = ScreenManager(self)

        self.loadScreen()

        self.screenManager.changeScreen('load')

    def run(self):
        self.running = True
        
        while self.running:
            self.handleEvents()

            self.render()

            self.update()

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

    def selectPlayer(self, player: str):
        self.save_system = SaveSystem(player)
        self.player_data = self.load_or_create_player_data()

    def load_or_create_player_data(self) -> PlayerData:
        save_data = self.save_system.load_game()

        if save_data is not None:
            return PlayerData(
                coins=save_data["coins"],
                owned_characters=save_data["owned_characters"],
                setting=save_data["setting"],
                rank=save_data["rank"],
                used_codes=save_data["used_codes"]
            )
        else :
            default_data = self.save_system.create_new_save()
            player_data = PlayerData(
                coins=default_data["coins"],
                owned_characters=default_data["owned_characters"],
                setting=default_data["setting"],
                rank=default_data["rank"],
                used_codes=default_data["used_codes"]
            )
            self.save_system.save_game(player_data)
            return player_data
