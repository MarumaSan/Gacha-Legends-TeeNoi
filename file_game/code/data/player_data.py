import json
import os
from pathlib import Path
from file_game.code.config import STARTING_COINS


class PlayerData:
    
    def __init__(self):
        self.coins = STARTING_COINS
        self.owned_heroes = set()
        self.settings = {
            'volume': 0.5,
            'sound_enabled': True
        }
        self.rank = 0
    
    def add_coins(self, amount: int) -> None:
        if amount > 0:
            self.coins += amount
    
    def spend_coins(self, amount: int) -> bool:
        if amount <= 0:
            return False
        
        if self.coins >= amount:
            self.coins -= amount
            return True
        return False
    
    def add_hero(self, hero_id: int) -> bool:
        if hero_id not in self.owned_heroes:
            self.owned_heroes.add(hero_id)
            return True
        return False
    
    def has_hero(self, hero_id: int) -> bool:
        return hero_id in self.owned_heroes
    
    def calculate_power(self) -> int:
        base_power_per_hero = 100
        return len(self.owned_heroes) * base_power_per_hero
    
    def get_coin_balance(self) -> int:
        return self.coins
    
    def get_owned_hero_count(self) -> int:
        return len(self.owned_heroes)
    
    def save_to_file(self, filepath: str = "file_game/json/save_data.json") -> bool:
        try:
            save_path = Path(filepath)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_data = {
                'coins': self.coins,
                'owned_heroes': list(self.owned_heroes),
                'settings': self.settings,
                'rank': self.rank
            }
            with open(filepath, 'w') as f:
                json.dump(save_data, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error saving player data: {e}")
            return False
    
    def load_from_file(self, filepath: str = "file_game/json/save_data.json") -> bool:
        try:
            if not os.path.exists(filepath):
                print(f"Save file not found: {filepath}")
                return False
            
            with open(filepath, 'r') as f:
                save_data = json.load(f)
            
            self.coins = save_data.get('coins', STARTING_COINS)
            self.owned_heroes = set(save_data.get('owned_heroes', []))
            self.settings = save_data.get('settings', {'volume': 0.5, 'sound_enabled': True})
            self.rank = save_data.get('rank', 0)
            
            return True
        except Exception as e:
            print(f"Error loading player data: {e}")
            return False
    
    def to_dict(self) -> dict:
        return {
            'coins': self.coins,
            'owned_heroes': list(self.owned_heroes),
            'settings': self.settings,
            'rank': self.rank
        }
    
    def from_dict(self, data: dict) -> None:
        self.coins = data.get('coins', STARTING_COINS)
        self.owned_heroes = set(data.get('owned_heroes', []))
        self.settings = data.get('settings', {'volume': 0.5, 'sound_enabled': True})
        self.rank = data.get('rank', 0)