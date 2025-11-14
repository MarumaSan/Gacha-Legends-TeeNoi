from dataclasses import field
from src.model.character import Character

class PlayerData:
    def __init__(self):
        self.coins: int = 1000
        self.owned_characters: set[str] = field(default_factory=set)
        self.setting: dict = field(default_factory=dict)
        self.rank: int = 0
        self.used_codes: set[str] = field(default_factory=set)

        self.setting['volume'] = 0

    def add_character(self, character: Character) -> None:
        if character.id not in self.owned_characters:
            self.owned_characters.add(character.id)

    def use_code(self, code: str, amount: int) -> bool:
        if code in self.used_codes:
            return False
        
        self.used_codes.add(code)
        self.coins += amount
        return True
    
    def setRank(self, rank: int) -> None:
        self.rank = rank

    def setVolume(self, volume_percent) -> None:
        self.setting['volume'] = volume_percent

    

