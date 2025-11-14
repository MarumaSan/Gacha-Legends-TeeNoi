import json
from src.utils.constants import PATH_SAVE
from typing import Optional, Any

class SaveSystem:
    def __init__(self, player: str):
        self.save_path = f'{PATH_SAVE}save_data_{player}.json'
    
    def save_game(self, player_data: Any) -> bool:
        try:
            save_data = {
                "coins": player_data.coins,
                "owned_characters": list(player_data.owned_characters),
                "setting": list(player_data.setting),
                "rank": player_data.rank,
                "used_codes": list(player_data.used_codes)
            }

            with open(self.save_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
        
    def load_game(self) -> Optional[dict[str, Any]]:
        try:
            with open(self.save_path, 'r', encoding='utf-8') as f:
                save_data = json.load(f)
            
            required_fields = [
                "coins",
                "owned_characters",
                "setting",
                "rank",
                "used_codes"
            ]
            
            for field in required_fields:
                if field not in save_data:
                    raise ValueError(f"Missing required field: {field}")
            
            save_data["owned_characters"] = set(save_data["owned_characters"])
            save_data["used_codes"] = set(save_data["used_codes"])
            
            return save_data

        except Exception as e:
            print(f"Error loading game: {e}")

    def create_new_save(self) -> dict[str, Any]:
        default_data = {
            "coins": 1000,
            "owned_characters": set(),
            "setting": set(),
            "rank": 0,
            "used_codes": set()
        }
        
        return default_data