import pygame
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PATH_UI,PATH_SOUND
from src.model.player_data import PlayerData
from src.core.save_system import SaveSystem
from src.core.screen_manager import ScreenManager
from src.screen.load_screen import LoadScreen
from src.screen.lobby_screen import LobbyScreen
from src.screen.setting_screen import SettingScreen
from src.screen.profile_screen import ProfileScreen
from src.screen.collection_screen import Collection


class GameManager:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()
        pygame.mixer.music.load(PATH_SOUND + 'bgm.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0)

        self.logo = pygame.image.load(PATH_UI + 'logo.png')

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Gacha Legends')
        pygame.display.set_icon(self.logo)

        self.clock = pygame.time.Clock()
        
        self.running = False

        self.save_systems: dict[str, SaveSystem] = {
            'player1': SaveSystem('player1'),
            'player2': SaveSystem('player2')
        }
        self.players: dict[str, PlayerData] = {
            'player1' : self.load_or_create_player_data(self.save_systems['player1']),
            'player2' : self.load_or_create_player_data(self.save_systems['player2'])
        }
        self.player_data = self.selectPlayer('player1')
        self.player_data = self.selectPlayer('player2')

        self.screenManager = ScreenManager(self)

        self.loadScreen()

        self.screenManager.changeScreen('collection')

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
        self.screenManager.loadScreen('profile', ProfileScreen(self))
        self.screenManager.loadScreen('collection', Collection(self))

    def selectPlayer(self, player: str) -> PlayerData:
        self.current_player_id = player
        self.player_data = self.players[player]
        return self.player_data
    
    def getPlayerData(self, player: str) -> PlayerData:
        self.player_data = self.players[player]
        return self.player_data


    def load_or_create_player_data(self, save_system: SaveSystem) -> PlayerData:
        save_data = save_system.load_game()

        if save_data is not None:
            return PlayerData(
                coins=save_data["coins"],
                owned_characters=save_data["owned_characters"],
                setting=save_data["setting"],
                rank=save_data["rank"],
                used_codes=save_data["used_codes"]
            )
        
        default_data = save_system.create_new_save()
        player_data = PlayerData(
            coins=default_data["coins"],
            owned_characters=default_data["owned_characters"],
            setting=default_data["setting"],
            rank=default_data["rank"],
            used_codes=default_data["used_codes"]
        )
        save_system.save_game(player_data)
        return player_data
