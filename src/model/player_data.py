from dataclasses import dataclass, field
from src.model.character import Character


@dataclass
class PlayerData:
    coins: int = 1000
    owned_characters: set[str] = field(default_factory=set)
    setting: dict = field(default_factory=lambda: {"volume": 0})
    win: int = 0
    used_codes: set[str] = field(default_factory=set)

    def add_character(self, character: Character) -> None:
        if character.id not in self.owned_characters:
            self.owned_characters.add(character.id)

    def use_code(self, code: str, amount: int) -> bool:
        if code in self.used_codes:
            return False
        
        self.used_codes.add(code)
        self.coins += amount
        return True
    
    def addWin(self, win: int) -> None:
        self.win += win

    def setVolume(self, volume_percent) -> None:
        self.setting['volume'] = volume_percent

        

    
