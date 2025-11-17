from dataclasses import dataclass
from typing import Dict

@dataclass
class GachaConfig:
    chest_type: str
    chest_name: str
    chest_path: str
    cost: int
    drop_rates: Dict[str, float]

mystic_chest = GachaConfig(
    chest_type= 'mystic',
    chest_name= 'Mystic Chest',
    chest_path= 'mystic_chest_background.png',
    cost=200,
    drop_rates={
        "rare": 90.0,
        "epic": 8.0,
        "legendary": 1.5,
        "extreme": 0.5
    }
)

celestial_chest = GachaConfig(
    chest_type= 'celestial',
    chest_name= 'Celestial Chest',
    chest_path= 'celestial_chest_background.png',
    cost=500,
    drop_rates={
        "rare": 70.0,
        "epic": 23.0,
        "legendary": 6.0,
        "extreme": 1.0
    }
)