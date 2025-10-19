import pygame
from game.game_state import GameState
from game.ui.button import Button
from game.ui.text_display import TextDisplay
from game.ui.animation import CardFlipAnimation, PulseAnimation, ParticleEffect
from game.systems.asset_manager import AssetManager
from game.systems.gacha_system import GachaSystem
from game.data.player_data import PlayerData
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_GOLD, SUMMON_COSTS


class GachaState(GameState):
    """Gacha screen for summoning heroes"""

    STATE_CHEST_SELECTION = "chest_selection"
    STATE_ANIMATING = "animating"
    STATE_RESULTS = "results"

    def __init__(self, game, player_data: PlayerData):
        super().__init__(game)
        self.assets = AssetManager()
        self.player_data = player_data
        self.gacha_system = GachaSystem()

        self.current_state = self.STATE_CHEST_SELECTION
        self.selected_chest = None

        self.background = None
        self.font_large = None
        self.font_normal = None
        self.font_small = None

        self.mystic_button = None
        self.celestial_button = None
        self.summon_x1_button = None
        self.summon_x10_button = None
        self.back_button = None
        self.return_button = None
        self.tap_to_continue_button = None
        self.back_to_lobby_button = None

        self.coin_display = None
        self.message_display = None

        self.summoned_heroes = []
        self.new_heroes = []
        self.current_card_index = 0

        self.animation_timer = 0.0
        self.card_flip_duration = 0.5
        self.show_card_back = True
        self.card_flip_anim = CardFlipAnimation(duration=0.6)
        self.new_hero_pulse = PulseAnimation(duration=1.0, min_scale=1.0, max_scale=1.1)
        self.particles = []

    def enter(self):
        try:
            self.background = self.assets.load_image('assets/backgrounds/summon_1.png',
                                                     (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Warning: Could not load background: {e}")
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((40, 20, 60))

        try:
            self.font_large = self.assets.load_font('assets/fonts/Monocraft.ttf', 36)
            self.font_normal = self.assets.load_font('assets/fonts/Monocraft.ttf', 24)
            self.font_small = self.assets.load_font('assets/fonts/Monocraft.ttf', 18)
        except Exception as e:
            print(f"Warning: Could not load font: {e}")
            self.font_large = pygame.font.Font(None, 36)
            self.font_normal = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 18)

        self.current_state = self.STATE_CHEST_SELECTION
        self.summoned_heroes = []
        self.new_heroes = []

        if hasattr(self.game, 'selected_chest_type') and self.game.selected_chest_type:
            self.selected_chest = self.game.selected_chest_type
            self.game.selected_chest_type = None
            self._create_summon_buttons()
        else:
            self.selected_chest = None

        self._create_chest_selection_ui()
        self._create_coin_display()

    def _create_chest_selection_ui(self):
        button_width = 250
        button_height = 80
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2

        self.mystic_button = Button(
            x=center_x - button_width - 30, y=center_y - button_height // 2,
            width=button_width, height=button_height,
            text="Mystic Chest", callback=lambda: self.select_chest('mystic'),
            font=self.font_normal, text_color=COLOR_WHITE,
            bg_color=(100, 60, 140), hover_color=(130, 90, 170)
        )
        self.celestial_button = Button(
            x=center_x + 30, y=center_y - button_height // 2,
            width=button_width, height=button_height,
            text="Celestial Chest", callback=lambda: self.select_chest('celestial'),
            font=self.font_normal, text_color=COLOR_WHITE,
            bg_color=(140, 100, 60), hover_color=(170, 130, 90)
        )
        self.return_button = Button(
            x=SCREEN_WIDTH - 220, y=SCREEN_HEIGHT - 80,
            width=200, height=60, text="Return to Lobby",
            callback=self.return_to_lobby, font=self.font_normal,
            text_color=COLOR_WHITE, bg_color=(70, 70, 120), hover_color=(100, 100, 150)
        )

    def _create_summon_buttons(self):
        button_width = 200
        button_height = 70
        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2 + 100

        cost_x1 = SUMMON_COSTS[f'{self.selected_chest}_x1']
        cost_x10 = SUMMON_COSTS[f'{self.selected_chest}_x10']

        self.summon_x1_button = Button(
            x=center_x - button_width - 20, y=center_y,
            width=button_width, height=button_height,
            text=f"x1 Summon\n{cost_x1} coins",
            callback=lambda: self.perform_summon(1),
            font=self.font_normal, text_color=COLOR_WHITE,
            bg_color=(60, 120, 60), hover_color=(90, 150, 90)
        )
        self.summon_x10_button = Button(
            x=center_x + 20, y=center_y,
            width=button_width, height=button_height,
            text=f"x10 Summon\n{cost_x10} coins",
            callback=lambda: self.perform_summon(10),
            font=self.font_normal, text_color=COLOR_WHITE,
            bg_color=(120, 60, 60), hover_color=(150, 90, 90)
        )
        self.back_button = Button(
            x=20, y=SCREEN_HEIGHT - 80, width=150, height=60,
            text="Back", callback=self.back_to_chest_selection,
            font=self.font_normal, text_color=COLOR_WHITE,
            bg_color=(70, 70, 70), hover_color=(100, 100, 100)
        )

    def _create_coin_display(self):
        self.coin_display = TextDisplay(
            text=f"Coins: {self.player_data.get_coin_balance()}",
            font=self.font_large, color=COLOR_GOLD, position=(20, 20)
        )

    def _create_message_display(self, message: str):
        self.message_display = TextDisplay(
            text=message, font=self.font_large, color=COLOR_WHITE,
            position=(SCREEN_WIDTH // 2, 100), align='center'
        )

    def select_chest(self, chest_type: str):
        print(f"Selected {chest_type} chest")
        self.selected_chest = chest_type
        self._create_summon_buttons()

    def back_to_chest_selection(self):
        self.selected_chest = None
        self.summon_x1_button = None
        self.summon_x10_button = None
        self.back_button = None
        self.message_display = None

    def return_to_lobby(self):
        if getattr(self.game.state_manager, "transitioning", False):
            return
        print("Returning to main lobby")
        if hasattr(self.game, "change_state_then_fade_in"):
            self.game.change_state_then_fade_in('main_lobby', duration=0.6)
        else:
            self.game.change_state('main_lobby')

    def perform_summon(self, count: int):
        cost_key = f'{self.selected_chest}_x{count}'
        cost = SUMMON_COSTS[cost_key]

        if not self.player_data.spend_coins(cost):
            print(f"Insufficient coins! Need {cost}, have {self.player_data.get_coin_balance()}")
            self._create_message_display("Not enough coins!")
            return

        print(f"Performing x{count} summon for {cost} coins")
        self.summoned_heroes = self.gacha_system.summon(count)
        self.new_heroes = []

        for hero in self.summoned_heroes:
            is_new = self.player_data.add_hero(hero.id)
            if is_new:
                self.new_heroes.append(hero)

        self.current_state = self.STATE_ANIMATING
        self.current_card_index = 0
        self.animation_timer = 0.0
        self.show_card_back = True
        self.card_flip_anim.start()
        self.particles = []

        if self.coin_display:
            self.coin_display.set_text(f"Coins: {self.player_data.get_coin_balance()}")

    def _update_animation(self, dt):
        self.animation_timer += dt
        flip_complete = self.card_flip_anim.update(dt)

        # อัปเดตพาร์ติเคิล
        self.particles = [p for p in self.particles if not p.update(dt)]

        # pulse เฉพาะตอนโชว์หน้าและเป็นฮีโร่ใหม่
        if not self.show_card_back and self.current_card_index < len(self.summoned_heroes):
            hero = self.summoned_heroes[self.current_card_index]
            if hero in self.new_heroes:
                self.new_hero_pulse.update(dt)

        if flip_complete:
            if self.card_flip_anim.is_back_visible():
                # จากหลัง -> กำลังจะโชว์หน้า
                self.show_card_back = False
                self.card_flip_anim.start()

                # celebration ถ้าเป็นฮีโร่ใหม่
                if self.current_card_index < len(self.summoned_heroes):
                    hero = self.summoned_heroes[self.current_card_index]
                    if hero in self.new_heroes:
                        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
                        self.particles.append(ParticleEffect((cx, cy), count=30))
            else:
                # หน้า -> ไปการ์ดถัดไป
                self.current_card_index += 1
                if self.current_card_index >= len(self.summoned_heroes):
                    self.current_state = self.STATE_RESULTS
                    self._create_tap_to_continue()
                else:
                    self.show_card_back = True
                    self.card_flip_anim.start()

    def _create_tap_to_continue(self):
        self.tap_to_continue_button = Button(
            x=SCREEN_WIDTH // 2 - 250, y=SCREEN_HEIGHT - 100,
            width=200, height=60, text="Continue", callback=self.finish_summon,
            font=self.font_normal, text_color=COLOR_WHITE,
            bg_color=(80, 80, 120), hover_color=(110, 110, 150)
        )
        self.back_to_lobby_button = Button(
            x=SCREEN_WIDTH // 2 + 50, y=SCREEN_HEIGHT - 100,
            width=200, height=60, text="Back to Lobby", callback=self.return_to_lobby,
            font=self.font_normal, text_color=COLOR_WHITE,
            bg_color=(70, 70, 120), hover_color=(100, 100, 150)
        )

    def finish_summon(self):
        print("Finishing summon")
        self.back_to_chest_selection()

    def handle_event(self, event):
        # บล็อกอีเวนต์ช่วงทรานซิชัน
        if getattr(self.game.state_manager, "transitioning", False):
            return

        if self.current_state == self.STATE_CHEST_SELECTION:
            if self.selected_chest is None:
                if self.mystic_button:
                    self.mystic_button.handle_event(event)
                if self.celestial_button:
                    self.celestial_button.handle_event(event)
            else:
                if self.summon_x1_button:
                    self.summon_x1_button.handle_event(event)
                if self.summon_x10_button:
                    self.summon_x10_button.handle_event(event)
                if self.back_button:
                    self.back_button.handle_event(event)

            if self.return_button:
                self.return_button.handle_event(event)

        elif self.current_state == self.STATE_RESULTS:
            if self.tap_to_continue_button:
                self.tap_to_continue_button.handle_event(event)
            if self.back_to_lobby_button:
                self.back_to_lobby_button.handle_event(event)

    def update(self, dt):
        # ไม่อัปเดตปุ่มช่วงทรานซิชัน (กัน hover กะพริบ)
        if getattr(self.game.state_manager, "transitioning", False):
            return

        if self.current_state == self.STATE_CHEST_SELECTION:
            if self.selected_chest is None:
                if self.mystic_button:
                    self.mystic_button.update(dt)
                if self.celestial_button:
                    self.celestial_button.update(dt)
            else:
                if self.summon_x1_button:
                    self.summon_x1_button.update(dt)
                if self.summon_x10_button:
                    self.summon_x10_button.update(dt)
                if self.back_button:
                    self.back_button.update(dt)

            if self.return_button:
                self.return_button.update(dt)

        elif self.current_state == self.STATE_ANIMATING:
            self._update_animation(dt)

        elif self.current_state == self.STATE_RESULTS:
            if self.tap_to_continue_button:
                self.tap_to_continue_button.update(dt)
            if self.back_to_lobby_button:
                self.back_to_lobby_button.update(dt)

        if self.coin_display:
            self.coin_display.set_text(f"Coins: {self.player_data.get_coin_balance()}")

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))

        if self.coin_display:
            self.coin_display.draw(screen)

        if self.current_state == self.STATE_CHEST_SELECTION:
            self._draw_chest_selection(screen)
        elif self.current_state == self.STATE_ANIMATING:
            self._draw_animation(screen)
        elif self.current_state == self.STATE_RESULTS:
            self._draw_results(screen)

    def _draw_chest_selection(self, screen):
        if self.selected_chest is None:
            if self.mystic_button:
                self.mystic_button.draw(screen)
            if self.celestial_button:
                self.celestial_button.draw(screen)

            title = self.font_large.render("Select a Chest", True, COLOR_WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
            screen.blit(title, title_rect)
        else:
            if self.summon_x1_button:
                self.summon_x1_button.draw(screen)
            if self.summon_x10_button:
                self.summon_x10_button.draw(screen)
            if self.back_button:
                self.back_button.draw(screen)

            chest_name = self.selected_chest.capitalize() + " Chest"
            title = self.font_large.render(chest_name, True, COLOR_WHITE)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
            screen.blit(title, title_rect)

        if self.return_button:
            self.return_button.draw(screen)

        if self.message_display:
            self.message_display.draw(screen)

    def _draw_animation(self, screen):
        if not self.summoned_heroes or self.current_card_index >= len(self.summoned_heroes):
            return

        hero = self.summoned_heroes[self.current_card_index]
        card_width, card_height = 300, 420
        card_y = SCREEN_HEIGHT // 2 - card_height // 2

        scale_x = self.card_flip_anim.get_scale_x()
        scaled_width = int(card_width * scale_x)
        show_back = self.card_flip_anim.is_back_visible()

        try:
            if show_back:
                card_back_path = f'assets/cards/back/{hero.rarity}.PNG'
                card_image = self.assets.load_image(card_back_path, (card_width, card_height))
            else:
                card_image = self.assets.load_image(hero.card_front_path, (card_width, card_height))

            if scaled_width > 0:
                scaled_card = pygame.transform.scale(card_image, (scaled_width, card_height))
                scaled_x = SCREEN_WIDTH // 2 - scaled_width // 2
                screen.blit(scaled_card, (scaled_x, card_y))
        except Exception as e:
            print(f"Warning: Could not load card image: {e}")
            if scaled_width > 0:
                scaled_x = SCREEN_WIDTH // 2 - scaled_width // 2
                pygame.draw.rect(screen, (100, 100, 100), (scaled_x, card_y, scaled_width, card_height))
                pygame.draw.rect(screen, COLOR_WHITE, (scaled_x, card_y, scaled_width, card_height), 3)

        if (not show_back) and (hero in self.new_heroes):
            pulse_scale = self.new_hero_pulse.get_scale()
            new_text = self.font_large.render("NEW HERO UNLOCKED!", True, COLOR_GOLD)
            sw, sh = int(new_text.get_width() * pulse_scale), int(new_text.get_height() * pulse_scale)
            scaled_text = pygame.transform.scale(new_text, (sw, sh))
            new_rect = scaled_text.get_rect(center=(SCREEN_WIDTH // 2, card_y - 50))

            bg_rect = new_rect.inflate(20, 10)
            bg = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
            bg.fill((0, 0, 0, 180))
            screen.blit(bg, bg_rect.topleft)
            screen.blit(scaled_text, new_rect)

            try:
                portrait_size = int(150 * pulse_scale)
                portrait = self.assets.load_image(hero.portrait_path, (portrait_size, portrait_size))
                portrait_x = SCREEN_WIDTH // 2 - portrait_size // 2
                portrait_y = card_y + card_height + 20
                screen.blit(portrait, (portrait_x, portrait_y))
            except Exception as e:
                print(f"Warning: Could not load portrait: {e}")

        for particle in self.particles:
            particle.draw(screen)

        progress_text = f"Card {self.current_card_index + 1} / {len(self.summoned_heroes)}"
        progress = self.font_normal.render(progress_text, True, COLOR_WHITE)
        progress_rect = progress.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(progress, progress_rect)

    def _draw_results(self, screen):
        title = self.font_large.render("Summon Complete!", True, COLOR_WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(title, title_rect)

        total_heroes = len(self.summoned_heroes)
        new_count = len(self.new_heroes)
        summary_text = f"Total: {total_heroes} heroes | New: {new_count}"
        summary = self.font_normal.render(summary_text, True, COLOR_WHITE)
        summary_rect = summary.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(summary, summary_rect)

        portrait_size = 100
        portraits_per_row = 5
        start_x = SCREEN_WIDTH // 2 - (min(portraits_per_row, total_heroes) * (portrait_size + 10)) // 2
        start_y = 220

        for i, hero in enumerate(self.summoned_heroes):
            row = i // portraits_per_row
            col = i % portraits_per_row
            x = start_x + col * (portrait_size + 10)
            y = start_y + row * (portrait_size + 10)
            try:
                portrait = self.assets.load_image(hero.portrait_path, (portrait_size, portrait_size))
                screen.blit(portrait, (x, y))
                if hero in self.new_heroes:
                    badge_text = self.font_small.render("NEW!", True, COLOR_GOLD)
                    badge_rect = badge_text.get_rect(center=(x + portrait_size // 2, y - 10))
                    bg_rect = badge_rect.inflate(10, 5)
                    pygame.draw.rect(screen, (0, 0, 0), bg_rect)
                    screen.blit(badge_text, badge_rect)
            except Exception as e:
                print(f"Warning: Could not load portrait for hero {hero.id}: {e}")
                pygame.draw.rect(screen, (80, 80, 80), (x, y, portrait_size, portrait_size))

        if self.tap_to_continue_button:
            self.tap_to_continue_button.draw(screen)
        if self.back_to_lobby_button:
            self.back_to_lobby_button.draw(screen)

    def exit(self):
        pass