import os
import random
from collections import defaultdict
import pygame
from src.ui.button import Button
from src.ui.text_display import TextDisplay
from src.ui.image import Image
from src.screen.base_screen import BaseScreen
from src.model.gacha_config import mystic_chest, celestial_chest
from src.utils.constants import COLOR_YELLOW, COLOR_PURPLE, CHARACTER

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game_manager import GameManager


CHARACTERS_BY_RARITY: dict[str, list] = defaultdict(list)
RARITY_BACK_PATH = {
    "rare": "assets/cards/back/rare.PNG",
    "epic": "assets/cards/back/legendary.PNG",
    "legendary": "assets/cards/back/legendary.PNG",
    "extreme": "assets/cards/back/extreme.PNG",
}
for character in CHARACTER:
    CHARACTERS_BY_RARITY[character.rarity].append(character)


class GachaScreen(BaseScreen):
    def __init__(self, manager: 'GameManager'):
        super().__init__(manager)

        self.setBackground('summon2.png')

        self.chest_screen_item: dict[str, list[Button | TextDisplay]] = {}
        self.drop_rate_screen_item: list[TextDisplay] = []

        self.buttons: list[Button] = []
        self.textDisplays: list[TextDisplay] = []
        self.card_images: list[Image] = []
        self.card_slots: list[dict] = []

        self.chest = mystic_chest
        self.chest_text_color = COLOR_YELLOW

        self._setup_ui()

    def _setup_ui(self) -> None:

        self.chest_screen_item = {
            'text' : [
                TextDisplay(
                    x=self.center_x,
                    y=210,
                    text='CHEST NAME',
                    size=80,
                    color=self.chest_text_color,
                ),
                TextDisplay(
                        x=self.center_x,
                        y=600,
                        text='Return to Lobby',
                        size=16,
                        callback=self.returnToLobby
                ),
                TextDisplay(
                    x=self.center_x - 120,
                    y=self.center_y - 40,
                    text='use coin',
                    size=16,
                    color=COLOR_YELLOW
                ),
                TextDisplay(
                    x=self.center_x + 120,
                    y=self.center_y - 40,
                    text='use coin',
                    size=16,
                    color=COLOR_YELLOW
                )
            ],
            'button' : [
                Button(
                    x=self.center_x - 120,
                    y=self.center_y + 50,
                    image_name=self.chest.chest_type + '_chest_background.png',
                    font_size=11,
                    text='SUMMON X1',
                    text_y=self.center_y + 98,
                    # callback=self.summon_x1
                ),
                Button(
                    x=self.center_x + 120,
                    y=self.center_y + 50,
                    image_name=self.chest.chest_type + '_chest_background.png',
                    font_size=11,
                    text='SUMMON X10',
                    text_y=self.center_y + 98,
                    # callback=self.summon_x10
                ),
                Button(
                    x=1240,
                    y=40,
                    image_name='mark.png',
                    callback=self.show_drop_rate
                )
            ]
        }

        self.drop_rate_screen_item = [
            TextDisplay(
                x=self.center_x,
                y=self.center_y,
                text='drop rate',
                size=16,
                enable=False
            ),
            TextDisplay(
                x=self.center_x,
                y= 600,
                text='back',
                size=16,
                enable=False,
                callback= self.show_chest_screen
            )
            
        ]

    def render(self, screen):
        screen.blit(self.background, (0, 0))

        for button in self.buttons:
            button.render(screen)

        for text in self.textDisplays:
            text.render(screen)

        for image in self.card_images:
            image.render(screen)

        for item in self.chest_screen_item.values():
            for data in item:
                data.render(screen)
        for item in self.drop_rate_screen_item:
            item.render(screen)

        self.update_transition(screen)
    
    def update(self):
        pass

    def handleEvents(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            for button in self.buttons:
                button.handleEvent(event)

            for text in self.textDisplays:
                text.handleEvent(event)

            for image in self.card_images:
                image.handleEvent(event)

            for item in self.chest_screen_item.values():
                for data in item:
                    data.handleEvent(event)
            
            for item in self.drop_rate_screen_item:
                item.handleEvent(event)

    def start_screen(self):
        if self.manager.chest_type not in ('mystic', 'celestial'):
            self.manager.chest_type = 'mystic'

        self.chest = mystic_chest if self.manager.chest_type == 'mystic' else celestial_chest

        chest_text_color = COLOR_YELLOW if self.chest.chest_type == 'mystic' else COLOR_PURPLE

        self.chest_screen_item['text'][0].setText(self.chest.chest_name)
        self.chest_screen_item['text'][0].setColor(chest_text_color)
        for i in range(2):
            self.chest_screen_item['button'][i].setImage(self.chest.chest_path)
        self.chest_screen_item['text'][2].setText(f'{self.chest.cost} COINS')
        self.chest_screen_item['text'][3].setText(f'{self.chest.cost * 10} COINS')



    def returnToLobby(self):
        self.manager.screenManager.changeScreen('lobby')

    def show_chest_screen(self):
        for data in self.chest_screen_item.values():
            for item in data:
                item.setEnable(True)
        
        for item in self.drop_rate_screen_item:
            item.setEnable(False)

    def show_drop_rate(self):
        for item in self.chest_screen_item.values():
            for data in item:
                data.setEnable(False)
        
        for item in self.drop_rate_screen_item:
            item.setEnable(True)
        
        self.drop_rate_screen_item[0].setText(
            f"Rare : {self.chest.drop_rates['rare']}% | Epic : {self.chest.drop_rates['epic']}% | "
            f"Legendary : {self.chest.drop_rates['legendary']}% | Extreme : {self.chest.drop_rates['extreme']}%"
        )

    # -------------------- Gacha Logic --------------------