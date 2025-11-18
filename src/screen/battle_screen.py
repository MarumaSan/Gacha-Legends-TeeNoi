import random
from src.ui.button import Button
from src.ui.text_display import TextDisplay
from src.ui.image import Image
from src.screen.base_screen import BaseScreen
from src.utils.constants import CHARACTER, COLOR_YELLOW, COLOR_RED

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game_manager import GameManager

ROUND_COUNT = 5
CHARACTER_BY_ID = {char.id: char for char in CHARACTER}


class BattleScreen(BaseScreen):
    def __init__(self, manager: 'GameManager'):
        super().__init__(manager)

        self.setBackground('arena.png')

        self.bet_amount = 100
        self.bet_step = 50
        self.min_bet = 50
        self.max_bet = 1000

        self.buttons: list[Button] = []
        self.result_texts: list[TextDisplay] = []

        self._setup_ui()

    # ------------------------------------------------------------------ UI SETUP

    def _setup_ui(self) -> None:
        self.message_display = TextDisplay(
            x=self.center_x,
            y=120,
            text='Set your bet and start the battle!',
            size=32,
            color=COLOR_YELLOW
        )

        self.player_label = TextDisplay(
            x=self.center_x - 250,
            y=180,
            text='PLAYER 1',
            size=20,
            color=COLOR_YELLOW
        )
        self.opponent_label = TextDisplay(
            x=self.center_x + 250,
            y=180,
            text='PLAYER 2',
            size=20,
            color=COLOR_YELLOW
        )

        for i in range(ROUND_COUNT):
            self.result_texts.append(
                TextDisplay(
                    x=self.center_x,
                    y=240 + (i * 40),
                    text='',
                    size=18
                )
            )

        self.bet_display = TextDisplay(
            x=self.center_x,
            y=440,
            text='Bet: 100 COINS EACH',
            size=22,
            color=COLOR_YELLOW
        )

        self.summary_display = TextDisplay(
            x=self.center_x,
            y=560,
            text='',
            size=24,
            color=COLOR_RED
        )

        placeholder_card = CHARACTER[0].card_front_path

        self.player_card_image = Image(
            x=self.center_x - 250,
            y=360,
            image_name=placeholder_card,
            path_prefix='',
            enable=False,
            scale=0.6
        )

        self.opponent_card_image = Image(
            x=self.center_x + 250,
            y=360,
            image_name=placeholder_card,
            path_prefix='',
            enable=False,
            scale=0.6
        )

        self.buttons = [
            Button(
                x=self.center_x - 200,
                y=500,
                image_name='wood1_background.png',
                text='- BET',
                font_size=14,
                callback=self.decrease_bet
            ),
            Button(
                x=self.center_x + 200,
                y=500,
                image_name='wood1_background.png',
                text='+ BET',
                font_size=14,
                callback=self.increase_bet
            ),
            Button(
                x=self.center_x,
                y=500,
                image_name='battle_button.png',
                callback=self.start_battle
            ),
            Button(
                x=self.center_x,
                y=660,
                image_name='wood1_background.png',
                text='RETURN TO LOBBY',
                font_size=14,
                callback=self.backToLobby
            )
        ]

    # ---------------------------------------------------------------- Rendering / Events

    def render(self, screen):
        screen.blit(self.background, (0, 0))

        self.message_display.render(screen)
        self.player_label.render(screen)
        self.opponent_label.render(screen)
        self.bet_display.render(screen)
        self.summary_display.render(screen)

        self.player_card_image.render(screen)
        self.opponent_card_image.render(screen)

        for text in self.result_texts:
            text.render(screen)

        for button in self.buttons:
            button.render(screen)

        self.update_transition(screen)
    
    def update(self):
        pass

    def handleEvents(self, events: list) -> None:
        for event in events:
            if self._dispatch_event(self.buttons, event):
                continue

    # ---------------------------------------------------------------- Battle Flow

    def start_screen(self):
        self.bet_amount = max(self.bet_amount, self.min_bet)
        self._update_player_labels()
        self._reset_results()
        self._update_bet_text()

    def backToLobby(self):
        self.manager.screenManager.changeScreen('lobby')

    def increase_bet(self):
        self.bet_amount = min(self.bet_amount + self.bet_step, self.max_bet)
        self._update_bet_text()

    def decrease_bet(self):
        self.bet_amount = max(self.bet_amount - self.bet_step, self.min_bet)
        self._update_bet_text()

    def start_battle(self):
        player = self.manager.player_data
        opponent_id = 'player1' if self.manager.current_player_id != 'player1' else 'player2'
        opponent = self.manager.players.get(opponent_id)

        if opponent is None:
            self._show_message("Opponent data not found.")
            return

        if len(player.owned_characters) < ROUND_COUNT:
            self._show_message("You need at least 5 heroes to battle.")
            return

        if len(opponent.owned_characters) < ROUND_COUNT:
            self._show_message("Opponent needs at least 5 heroes.")
            return

        if player.coins < self.bet_amount:
            self._show_message("Not enough coins for your bet.")
            return

        if opponent.coins < self.bet_amount:
            self._show_message("Opponent does not have enough coins.")
            return

        player_ids = random.sample(list(player.owned_characters), ROUND_COUNT)
        opponent_ids = random.sample(list(opponent.owned_characters), ROUND_COUNT)

        player.coins -= self.bet_amount
        opponent.coins -= self.bet_amount
        pot = self.bet_amount * 2

        player_score = 0
        opponent_score = 0

        for idx in range(ROUND_COUNT):
            hero_player = CHARACTER_BY_ID.get(player_ids[idx])
            hero_opponent = CHARACTER_BY_ID.get(opponent_ids[idx])

            if hero_player is None or hero_opponent is None:
                continue

            player_power = hero_player.totalPower
            opponent_power = hero_opponent.totalPower

            if player_power > opponent_power:
                winner_text = "You win the round!"
                player_score += 1
            elif player_power < opponent_power:
                winner_text = "Opponent wins the round."
                opponent_score += 1
            else:
                winner_text = "Round tied."

            self.result_texts[idx].setText(
                f'Round {idx + 1}: {hero_player.name} ({player_power}) vs {hero_opponent.name} ({opponent_power}) -> {winner_text}'
            )

            current_player_card = hero_player.card_front_path
            current_opponent_card = hero_opponent.card_front_path

            self.player_card_image.setEnable(True)
            self.opponent_card_image.setEnable(True)
            self.player_card_image.setImage(hero_player.card_front_path)
            self.opponent_card_image.setImage(hero_opponent.card_front_path)

        if player_score > opponent_score:
            player.coins += pot
            player.win += 1
            summary = f'You win the match! Score {player_score} - {opponent_score}'
        elif player_score < opponent_score:
            opponent.coins += pot
            opponent.win += 1
            summary = f'Opponent wins the match! Score {player_score} - {opponent_score}'
        else:
            player.coins += self.bet_amount
            opponent.coins += self.bet_amount
            summary = f'Match tied! Score {player_score} - {opponent_score}'

        self.summary_display.setText(summary)
        self._show_message("Battle complete.")
        self._update_player_labels()
        self._update_bet_text()

        self.manager.save_systems[self.manager.current_player_id].save_game(player)
        self.manager.save_systems[opponent_id].save_game(opponent)

    # ---------------------------------------------------------------- Helpers

    def _update_player_labels(self) -> None:
        player = self.manager.player_data
        opponent_id = 'player1' if self.manager.current_player_id != 'player1' else 'player2'
        opponent = self.manager.players.get(opponent_id)

        player_name = self._format_player_name(self.manager.current_player_id)
        opponent_name = self._format_player_name(opponent_id)

        self.player_label.setText(f'{player_name} | Coins {player.coins} | Wins {player.win}')

        if opponent:
            self.opponent_label.setText(f'{opponent_name} | Coins {opponent.coins} | Wins {opponent.win}')
        else:
            self.opponent_label.setText(f'{opponent_name} | No data')

    def _reset_results(self) -> None:
        for text in self.result_texts:
            text.setText('')
        self.summary_display.setText('')

    def _update_bet_text(self) -> None:
        self.bet_display.setText(f'Bet: {self.bet_amount} COINS EACH')

    def _show_message(self, message: str) -> None:
        self.message_display.setText(message)

    @staticmethod
    def _format_player_name(player_id: str) -> str:
        return player_id.replace('player', 'Player ')
