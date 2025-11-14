"""
Scene manager for handling scene transitions and lifecycle.
"""
from typing import Dict, Optional, TYPE_CHECKING
from src.screen.base_screen import BaseScreen

if TYPE_CHECKING:
    from src.core.game_manager import GameManager


class ScreenManager:
    
    def __init__(self, game_manager: 'GameManager'):
        self.game_manager = game_manager
        self.screen: Dict[str, BaseScreen] = {}
        self.currentScreen: Optional[BaseScreen] = None
    
    def loadScreen(self, name: str, screen: BaseScreen) -> None:
        self.screen[name] = screen
    
    def changeScreen(self, scene_name: str) -> None:
        self.currentScreen = self.screen[scene_name]