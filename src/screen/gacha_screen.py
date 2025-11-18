import random
import pygame
from src.ui.button import Button
from src.ui.text_display import TextDisplay
from src.screen.base_screen import BaseScreen
from src.model.gacha_config import mystic_chest, celestial_chest
from src.utils.constants import COLOR_YELLOW, COLOR_PURPLE, COLOR_RED, CHARACTER
from src.model.character import Character
from src.ui.load_image import LoadImage

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game_manager import GameManager


class GachaScreen(BaseScreen):
    def __init__(self, manager: 'GameManager'):
        super().__init__(manager)

        self.setBackground('summon2.png')

        self.chest_widgets: list[Button | TextDisplay] = []
        self.drop_rate_widgets: list[TextDisplay] = []
        self.summon_widgets: list[TextDisplay] = []
        self.card_images: list[LoadImage] = []

        self.chest = mystic_chest
        self.roll_character: list[Character] | None = None

        self.character_pool = {
            "rare": [c for c in CHARACTER if c.rarity == "rare"],
            "epic": [c for c in CHARACTER if c.rarity == "epic"],
            "legendary": [c for c in CHARACTER if c.rarity == "legendary"],
            "extreme": [c for c in CHARACTER if c.rarity == "extreme"],
        }

        self._setup_ui()

    # ------------------------------------------------------------------ UI SETUP

    def _setup_ui(self) -> None:
        self._build_chest_widgets()
        self._build_drop_rate_widgets()
        self._build_summon_widgets()

    def _build_chest_widgets(self) -> None:
        self.chest_title = TextDisplay(
            x=self.center_x,
            y=210,
            text='CHEST NAME',
            size=80,
            color=COLOR_YELLOW,
        )
        self.return_to_lobby_text = TextDisplay(
            x=self.center_x,
            y=600,
            text='Return to Lobby',
            size=16,
            callback=self.returnToLobby
        )
        self.single_cost_text = TextDisplay(
            x=self.center_x - 120,
            y=self.center_y - 40,
            text='use coin',
            size=16,
            color=COLOR_YELLOW
        )
        self.multi_cost_text = TextDisplay(
            x=self.center_x + 120,
            y=self.center_y - 40,
            text='use coin',
            size=16,
            color=COLOR_YELLOW
        )
        self.single_summon_button = Button(
            x=self.center_x - 120,
            y=self.center_y + 50,
            image_name=self.chest.chest_path,
            font_size=11,
            text='SUMMON X1',
            text_y=self.center_y + 98,
            callback=self.summon_x1
        )
        self.multi_summon_button = Button(
            x=self.center_x + 120,
            y=self.center_y + 50,
            image_name=self.chest.chest_path,
            font_size=11,
            text='SUMMON X10',
            text_y=self.center_y + 98,
            callback=self.summon_x10
        )
        self.drop_rate_button = Button(
            x=1240,
            y=40,
            image_name='mark.png',
            callback=self.drop_rate_phase
        )

        self.chest_widgets = [
            self.chest_title,
            self.return_to_lobby_text,
            self.single_cost_text,
            self.multi_cost_text,
            self.single_summon_button,
            self.multi_summon_button,
            self.drop_rate_button,
        ]

    def _build_drop_rate_widgets(self) -> None:
        self.drop_rate_text = TextDisplay(
            x=self.center_x,
            y=self.center_y,
            text='drop rate',
            size=16,
            enable=False
        )
        self.drop_rate_back = TextDisplay(
            x=self.center_x,
            y=600,
            text='BACK',
            size=16,
            enable=False,
            callback=self.chest_phase
        )
        self.drop_rate_widgets = [self.drop_rate_text, self.drop_rate_back]

    def _build_summon_widgets(self) -> None:
        self.summon_feedback_text = TextDisplay(
            x=self.center_x,
            y=530,
            text='feedback',
            size=16,
            color=COLOR_RED,
            enable=False
        )
        self.summon_prompt_text = TextDisplay(
            x=self.center_x,
            y=600,
            text='TAP TO REVEAL!',
            size=16,
            enable=False,
            callback=self.open_card
        )
        self.summon_back_text = TextDisplay(
            x=self.center_x,
            y=600,
            text='TAP TO BACK',
            size=16,
            callback=self.close_card,
            enable=False
        )
        self.summon_widgets = [
            self.summon_feedback_text,
            self.summon_prompt_text,
            self.summon_back_text,
        ]

    # ---------------------------------------------------------------- Rendering / Events

    def render(self, screen):
        screen.blit(self.background, (0, 0))

        self._render_group(screen, self.chest_widgets)
        self._render_group(screen, self.drop_rate_widgets)
        self._render_group(screen, self.card_images)
        self._render_group(screen, self.summon_widgets)

        self.update_transition(screen)
    
    def _render_group(self, screen: pygame.Surface, group: list) -> None:
        for widget in group:
            widget.render(screen)

    def update(self):
        pass

    def handleEvents(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            for group in self._event_layers():
                if self._dispatch_event(group, event):
                    break

    def _event_layers(self) -> list[list]:
        return [
            self.summon_widgets,
            self.card_images,
            self.drop_rate_widgets,
            self.chest_widgets,
        ]

    # ---------------------------------------------------------------- Screen transitions

    def start_screen(self):
        self.card_images.clear()
        self.roll_character = None
        self.summon_set_screen(False)
        self.summon_back_text.setEnable(False)
        self._show_feedback(None)

        if self.manager.chest_type not in ('mystic', 'celestial'):
            self.manager.chest_type = 'mystic'

        self.chest = mystic_chest if self.manager.chest_type == 'mystic' else celestial_chest

        chest_text_color = COLOR_YELLOW if self.chest.chest_type == 'mystic' else COLOR_PURPLE
        self.chest_title.setText(self.chest.chest_name)
        self.chest_title.setColor(chest_text_color)

        for button in (self.single_summon_button, self.multi_summon_button):
            button.setImage(self.chest.chest_path)

        self.single_cost_text.setText(f'{self.chest.cost} COINS')
        self.multi_cost_text.setText(f'{self.chest.cost * 10} COINS')

        self.chest_phase()

    def returnToLobby(self):
        self.manager.screenManager.changeScreen('lobby')

    def chest_phase(self):
        self.chest_set_screen(True)
        self.drop_rate_set_screen(False)

    def drop_rate_phase(self):
        self.chest_set_screen(False)
        self.drop_rate_set_screen(True)

        rates = self.chest.drop_rates
        self.drop_rate_text.setText(
            f"Rare : {rates['rare']}% | Epic : {rates['epic']}% | "
            f"Legendary : {rates['legendary']}% | Extreme : {rates['extreme']}%"
        )

    def chest_set_screen(self, enable: bool):
        self._set_group_enable(self.chest_widgets, enable)

    def drop_rate_set_screen(self, enable: bool):
        self._set_group_enable(self.drop_rate_widgets, enable)

    def summon_set_screen(self, enable: bool):
        for item in self.card_images:
            item.setEnable(enable)
        self.summon_prompt_text.setEnable(enable)

    def _set_group_enable(self, group: list, enable: bool) -> None:
        for widget in group:
            widget.setEnable(enable)

    # --------------------------------------------------------------------- Gacha logic

    def _show_feedback(self, message: str | None) -> None:
        if not message:
            self.summon_feedback_text.setEnable(False)
            return
        self.summon_feedback_text.setText(message)
        self.summon_feedback_text.setEnable(True)

    def _spend_coins(self, amount: int) -> bool:
        if self.manager.player_data.coins < amount:
            self._show_feedback('NOT ENOUGH COINS')
            return False
        self.manager.player_data.coins -= amount
        self._show_feedback(None)
        return True

    def roll(self) -> str:
        total = sum(self.chest.drop_rates.values())
        rnd = random.uniform(0, total)

        current = 0
        for rarity, rate in self.chest.drop_rates.items():
            current += rate
            if rnd <= current:
                return rarity
        return "rare"

    def _pull_characters(self, count: int) -> list[Character]:
        results: list[Character] = []
        for _ in range(count):
            rarity = self.roll()
            pool = self.character_pool[rarity]
            results.append(random.choice(pool))
        return results
    
    def summon_x1(self):
        if not self._spend_coins(self.chest.cost):
            return

        self.roll_character = self._pull_characters(1)

        self.manager.player_data.add_character(self.roll_character[0])

        self.card_images.clear()
        self.card_images.append(
            LoadImage(
                x=self.center_x,
                y=self.center_y,
                path=self.roll_character[0].card_back_path,
                scale=0.4,
                callback=self.open_card
            )
        )

        self.summon_set_screen(True)
        self.summon_back_text.setEnable(False)
        self.chest_set_screen(False)
        self.drop_rate_set_screen(False)
    
    def summon_x10(self):
        cost = self.chest.cost * 10
        if not self._spend_coins(cost):
            return

        self.roll_character = self._pull_characters(10)

        for character in self.roll_character:
            self.manager.player_data.add_character(character)

        start_x, start_y = 280, 200
        gap_x, gap_y = 180, 250
        
        self.card_images.clear()
        for i in range(len(self.roll_character)):
            row = i // 5
            col = i % 5
            x = start_x + col * gap_x
            y = start_y + row * gap_y

            self.card_images.append(
                LoadImage(
                    x=x,
                    y=y,
                    path=self.roll_character[i].card_back_path,
                    scale=0.25,
                    callback=self.open_card
                )
            )

        self.summon_set_screen(True)
        self.summon_back_text.setEnable(False)
        self.chest_set_screen(False)
        self.drop_rate_set_screen(False)

    def open_card(self):
        if not self.roll_character:
            return
        
        self.manager.save_systems[self.manager.current_player_id].save_game(self.manager.player_data)

        for i, image in enumerate(self.card_images):
            image.setImage(self.roll_character[i].card_front_path)
        
        self.summon_prompt_text.setEnable(False)
        self.summon_back_text.setEnable(True)
        for image in self.card_images:
            image.callback = self.close_card

    def close_card(self):
        self.summon_set_screen(False)
        self.summon_back_text.setEnable(False)
        self.chest_phase()
