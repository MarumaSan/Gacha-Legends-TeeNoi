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

        self.buttons: list[Button] = []
        self.textDisplays: list[TextDisplay] = []
        self.card_images: list[Image] = []
        self.card_slots: list[dict] = []

        self.chest = mystic_chest
        self.chest_text_color = COLOR_YELLOW

        self._setup_ui()

    def _setup_ui(self) -> None:
        self.textDisplays = [
            TextDisplay(
                x=self.center_x,
                y=210,
                text='CHEST NAME',
                size=80,
                color=self.chest_text_color,
                callback=self.returnToLobby
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
                text='coin',
                size=16,
                color=COLOR_YELLOW
            ),
            TextDisplay(
                x=self.center_x + 120,
                y=self.center_y - 40,
                text='coin',
                size=16,
                color=COLOR_YELLOW
            ),
            TextDisplay(
                x=self.center_x,
                y=self.center_y + 100,
                text='back',
                size=16,
                callback=self.openLayout1,
                enable=False
            ),
            TextDisplay(
                x=self.center_x,
                y=self.center_y,
                text='drop rate',
                size=16,
                enable=False
            ),
            TextDisplay(
                x=self.center_x,
                y=self.center_y + 160,
                text='',
                size=18,
                color=COLOR_YELLOW
            )
        ]

        self.buttons = [
            Button(
                x=self.center_x - 120,
                y=self.center_y + 50,
                image_name=self.chest.chest_type + '_chest_background.png',
                font_size=11,
                text='SUMMON X1',
                text_y=self.center_y + 98,
                callback=self.summon_x1
            ),
            Button(
                x=self.center_x + 120,
                y=self.center_y + 50,
                image_name=self.chest.chest_type + '_chest_background.png',
                font_size=11,
                text='SUMMON X10',
                text_y=self.center_y + 98,
                callback=self.summon_x10
            ),
            Button(
                x=1240,
                y=40,
                image_name='mark.png',
                callback=self.mark
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

    def start_screen(self):
        if self.manager.chest_type not in ('mystic', 'celestial'):
            self.manager.chest_type = 'mystic'

        self.chest = mystic_chest if self.manager.chest_type == 'mystic' else celestial_chest

        chest_text_color = COLOR_YELLOW if self.chest.chest_type == 'mystic' else COLOR_PURPLE
        self.textDisplays[0].setText(self.chest.chest_name)
        self.textDisplays[0].setColor(chest_text_color)

        for i in range(2):
            self.buttons[i].setImage(f'{self.chest.chest_path}')

        self.textDisplays[2].setText(f'{self.chest.cost} COINS')
        self.textDisplays[3].setText(f'{self.chest.cost * 10} COINS')
        self.card_images.clear()
        self.card_slots.clear()
        self._show_result('Tap Summon to draw cards!')

    def returnToLobby(self):
        self.manager.screenManager.changeScreen('lobby')

    def mark(self):
        self.closeLayout1()
        self.textDisplays[4].setEnable(True)
        self.textDisplays[5].setEnable(True)
        self.textDisplays[5].setText(
            f"Rare : {self.chest.drop_rates['rare']}% | Epic : {self.chest.drop_rates['epic']}% | "
            f"Legendary : {self.chest.drop_rates['legendary']}% | Extreme : {self.chest.drop_rates['extreme']}%"
        )
        
    def closeLayout1(self):
        for i in range(4):
            self.textDisplays[i].setEnable(False)
        for i in range(3):
            self.buttons[i].setEnable(False)
        self.textDisplays[6].setEnable(True)

    def openLayout1(self):
        for text in self.textDisplays:
            text.setEnable(False)

        for image in self.card_images:
            image.setEnable(False)

        for i in range(4):
            self.textDisplays[i].setEnable(True)
        for i in range(3):
            self.buttons[i].setEnable(True)
        self.textDisplays[6].setEnable(True)
        for image in self.card_images:
            image.setEnable(True)

    # -------------------- Gacha Logic --------------------
    def summon_x1(self):
        self._perform_summon(1)

    def summon_x10(self):
        self._perform_summon(10)

    def _perform_summon(self, count: int) -> None:
        cost = self.chest.cost * count

        if not self._can_afford(cost):
            self._show_result(f"Not enough coins for x{count}.", error=True)
            return

        self._pay(cost)

        pulls = []
        pulled_characters: list = []
        for _ in range(count):
            rarity, character = self._roll_one_character()
            already_owned = character.name in self.manager.player_data.owned_characters
            self.manager.player_data.add_character(character)
            pulls.append(f"{character.name} [{rarity.title()}]{' *NEW*' if not already_owned else ''}")
            pulled_characters.append(character)

        self._save_progress()

        summary = "X1 → " + pulls[0] if count == 1 else "X10 → " + ", ".join(pulls)
        summary += f" | Coins left: {self.manager.player_data.coins}"
        self._show_result(summary)
        self._display_cards(pulled_characters)

    def _can_afford(self, cost: int) -> bool:
        return self.manager.player_data.coins >= cost

    def _pay(self, cost: int) -> None:
        self.manager.player_data.coins -= cost

    def _roll_one_character(self):
        rarity = self._roll_rarity()
        pool = CHARACTERS_BY_RARITY.get(rarity, [])
        if not pool:
            pool = CHARACTER
        character = random.choice(pool)
        return rarity, character

    def _roll_rarity(self) -> str:
        total = sum(self.chest.drop_rates.values())
        pick = random.uniform(0, total)
        current = 0.0
        for rarity, rate in self.chest.drop_rates.items():
            current += rate
            if pick <= current:
                return rarity
        return list(self.chest.drop_rates.keys())[-1]

    def _save_progress(self):
        current_player = getattr(self.manager, 'current_player_id', None)
        if current_player is None:
            return
        save_system = self.manager.save_systems[current_player]
        save_system.save_game(self.manager.player_data)

    def _show_result(self, message: str, error: bool = False) -> None:
        color = (255, 99, 99) if error else COLOR_YELLOW
        self.textDisplays[6].setColor(color)
        self.textDisplays[6].setText(message)

    def _display_cards(self, characters: list) -> None:
        self.card_images.clear()
        self.card_slots.clear()

        if not characters:
            return

        total_cards = len(characters)
        cols = 5 if total_cards > 1 else 1
        rows = (total_cards + cols - 1) // cols
        spacing_x = 120
        spacing_y = 160
        start_x = self.center_x - ((cols - 1) * spacing_x) / 2
        start_y = self.center_y - ((rows - 1) * spacing_y) / 2

        for idx, character in enumerate(characters):
            row = idx // cols
            col = idx % cols
            x = int(start_x + col * spacing_x)
            y = int(start_y + row * spacing_y)

            card_image = Image(
                x=x,
                y=y,
                image_name=self._resolve_back_path(character),
                path_prefix='',
                scale=0.45 if len(characters) > 1 else 0.7,
                callback=lambda index=idx: self._flip_card(index)
            )

            slot = {
                "image": card_image,
                "character": character,
                "scale": card_image._scale,
                "revealed": False
            }

            self.card_images.append(card_image)
            self.card_slots.append(slot)

    def _flip_card(self, index: int) -> None:
        if index >= len(self.card_slots):
            return

        slot = self.card_slots[index]
        if slot["revealed"]:
            return

        slot["revealed"] = True
        slot["image"].path_prefix = ''
        scale = slot["scale"]
        slot["image"].setImage(self._resolve_front_path(slot["character"]))
        slot["image"].setScale(scale)
        self._show_result(f"{slot['character'].name} [{slot['character'].rarity.title()}]")

    def _resolve_back_path(self, character) -> str:
        candidate = character.card_back_path
        if candidate and os.path.exists(candidate):
            return candidate
        return RARITY_BACK_PATH.get(character.rarity, "assets/cards/back/rare.PNG")

    def _resolve_front_path(self, character) -> str:
        candidate = character.card_front_path
        if candidate and os.path.exists(candidate):
            return candidate
        return "assets/cards/front/hero1.png"
