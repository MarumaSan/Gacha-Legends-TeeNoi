from math import sqrt, pow

class Character:
    def __init__(self, id: int, name: str, rarity: str, atk: int, defense: int, portrait_path: str, card_front_path: str, card_back_path: str):
        self.id = id
        self.name = name
        self.rarity = rarity
        self.atk = atk
        self.defense = defense
        self.totalPower = round(sqrt(pow(self.atk, 2) + pow(self.defense, 2)))
        self.portrait_path = portrait_path
        self.card_front_path = card_front_path
        self.card_back_path = card_back_path