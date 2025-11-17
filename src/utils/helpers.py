from src.utils.constants import CHARACTER

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game_manager import GameManager

CHARACTER_BY_ID = {char.id: char for char in CHARACTER}

class Helpers():
    def __init__(self, manager: 'GameManager'):
        self.manager = manager

    def get_total_power(self, Player: str):
        total = 0
        for hero_id in self.manager.getPlayerData(Player).owned_characters:
            hero = CHARACTER_BY_ID.get(hero_id)
            if hero:
                total += hero.totalPower
        return total