"""
Scene manager for handling scene transitions and lifecycle.
"""
from typing import Dict, Optional, TYPE_CHECKING
from src.screen.base_screen import BaseScreen

if TYPE_CHECKING:
    from src.core.game_manager import GameManager


class ScreenManager:
    
    def __init__(self, manager: 'GameManager'):
        self.manager = manager
        self.screen: Dict[str, BaseScreen] = {}
        self.currentScreen: Optional[BaseScreen] = None
    
    def loadScreen(self, name: str, screen: BaseScreen) -> None:
        self.screen[name] = screen
    
    def changeScreen(self, screen_name: str) -> None:
        if self.currentScreen is not None:
            self.currentScreen.on_exit()

        self.currentScreen = self.screen[screen_name]

        self.manager.save_systems[self.manager.current_player_id].save_game(self.manager.player_data)

        self.currentScreen.on_enter()