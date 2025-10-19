"""Book state - displays hero collection with pagination and details"""

import pygame
from game.game_state import GameState
from game.ui.button import Button
from game.ui.text_display import TextDisplay
from game.systems.asset_manager import AssetManager
from game.data.player_data import PlayerData
from game.data.hero_data import get_hero, get_all_heroes
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLOR_WHITE, COLOR_GOLD


class BookState(GameState):
    """Book screen displaying hero collection with pagination and details"""

    def __init__(self, game, player_data: PlayerData):
        super().__init__(game)
        self.assets = AssetManager()
        self.player_data = player_data
        self.background = None
        self.font_large = None
        self.font_normal = None
        self.font_small = None

        # Pagination
        self.current_page = 0
        self.heroes_per_page = 12
        self.total_heroes = len(get_all_heroes())
        self.total_pages = (self.total_heroes + self.heroes_per_page - 1) // self.heroes_per_page

        # UI
        self.prev_button = None
        self.next_button = None
        self.back_button = None
        self.page_display = None

        # Hero slots
        self.hero_slots = []  # (rect, hero_id, is_owned)

        # Details
        self.selected_hero = None
        self.detail_panel_rect = None
        self.detail_close_button = None

    def enter(self):
        try:
            self.background = self.assets.load_image('assets/backgrounds/book.png', (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception as e:
            print(f"Warning: Could not load background: {e}")
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((40, 30, 20))

        try:
            self.font_large = self.assets.load_font('assets/fonts/Monocraft.ttf', 32)
            self.font_normal = self.assets.load_font('assets/fonts/Monocraft.ttf', 20)
            self.font_small = self.assets.load_font('assets/fonts/Monocraft.ttf', 16)
        except Exception as e:
            print(f"Warning: Could not load font: {e}")
            self.font_large = pygame.font.Font(None, 32)
            self.font_normal = pygame.font.Font(None, 20)
            self.font_small = pygame.font.Font(None, 16)

        if hasattr(self.game, 'selected_hero_id') and self.game.selected_hero_id:
            hero_id = self.game.selected_hero_id
            self.game.selected_hero_id = None
            if self.player_data.has_hero(hero_id):
                self.selected_hero = get_hero(hero_id)
                self._create_detail_panel()

        self._create_buttons()
        self._create_hero_slots()
        self._create_page_display()

    def _create_buttons(self):
        button_width = 120
        button_height = 50

        self.prev_button = Button(
            x=50, y=SCREEN_HEIGHT - 100, width=button_width, height=button_height,
            text="< Prev", callback=self.on_prev_page, font=self.font_normal,
            text_color=COLOR_WHITE, bg_color=(80, 60, 40), hover_color=(110, 90, 70)
        )
        self.next_button = Button(
            x=SCREEN_WIDTH - 170, y=SCREEN_HEIGHT - 100, width=button_width, height=button_height,
            text="Next >", callback=self.on_next_page, font=self.font_normal,
            text_color=COLOR_WHITE, bg_color=(80, 60, 40), hover_color=(110, 90, 70)
        )
        self.back_button = Button(
            x=SCREEN_WIDTH // 2 - 80, y=SCREEN_HEIGHT - 100, width=160, height=button_height,
            text="Return", callback=self.on_back_click, font=self.font_normal,
            text_color=COLOR_WHITE, bg_color=(100, 70, 50), hover_color=(130, 100, 80)
        )

    def _create_hero_slots(self):
        self.hero_slots = []
        cols, rows = 4, 3
        slot_size = 140
        slot_spacing = 20

        grid_width = cols * slot_size + (cols - 1) * slot_spacing
        grid_height = rows * slot_size + (rows - 1) * slot_spacing
        start_x = (SCREEN_WIDTH - grid_width) // 2
        start_y = 120

        start_idx = self.current_page * self.heroes_per_page
        end_idx = min(start_idx + self.heroes_per_page, self.total_heroes)

        for i in range(start_idx, end_idx):
            hero_id = i + 1
            row = (i - start_idx) // cols
            col = (i - start_idx) % cols
            x = start_x + col * (slot_size + slot_spacing)
            y = start_y + row * (slot_size + slot_spacing)
            rect = pygame.Rect(x, y, slot_size, slot_size)
            is_owned = self.player_data.has_hero(hero_id)
            self.hero_slots.append((rect, hero_id, is_owned))

    def _create_page_display(self):
        page_text = f"Page {self.current_page + 1}/{self.total_pages}"
        self.page_display = TextDisplay(
            text=page_text, font=self.font_normal, color=COLOR_WHITE,
            position=(SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT - 150)
        )

    def on_prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self._create_hero_slots()
            self._create_page_display()

    def on_next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
            self._create_hero_slots()
            self._create_page_display()

    def on_back_click(self):
        """Return to main lobby (เปลี่ยนก่อน -> เฟดเข้า)"""
        if getattr(self.game.state_manager, "transitioning", False):
            return
        self.selected_hero = None
        if hasattr(self.game, "change_state_then_fade_in"):
            self.game.change_state_then_fade_in('main_lobby', duration=0.6)
        else:
            self.game.change_state('main_lobby')

    def on_hero_click(self, hero_id: int):
        if self.player_data.has_hero(hero_id):
            self.selected_hero = get_hero(hero_id)
            self._create_detail_panel()

    def _create_detail_panel(self):
        if not self.selected_hero:
            return
        panel_width, panel_height = 500, 600
        panel_x = (SCREEN_WIDTH - panel_width) // 2
        panel_y = (SCREEN_HEIGHT - panel_height) // 2
        self.detail_panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        self.detail_close_button = Button(
            x=panel_x + panel_width - 120, y=panel_y + panel_height - 60,
            width=100, height=40, text="Close", callback=self.on_close_details,
            font=self.font_normal, text_color=COLOR_WHITE,
            bg_color=(100, 70, 50), hover_color=(130, 100, 80)
        )

    def on_close_details(self):
        self.selected_hero = None
        self.detail_close_button = None

    def handle_event(self, event):
        # บล็อกอีเวนต์ช่วงทรานซิชัน
        if getattr(self.game.state_manager, "transitioning", False):
            return

        if self.selected_hero and self.detail_close_button:
            self.detail_close_button.handle_event(event)
            return

        if self.prev_button:
            self.prev_button.handle_event(event)
        if self.next_button:
            self.next_button.handle_event(event)
        if self.back_button:
            self.back_button.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for rect, hero_id, is_owned in self.hero_slots:
                if rect.collidepoint(mouse_pos) and is_owned:
                    self.on_hero_click(hero_id)
                    break

    def update(self, dt):
        # ไม่อัปเดตปุ่มช่วงทรานซิชัน (กัน hover กะพริบ)
        if getattr(self.game.state_manager, "transitioning", False):
            return

        if self.selected_hero and self.detail_close_button:
            self.detail_close_button.update(dt)
        else:
            if self.prev_button:
                self.prev_button.update(dt)
            if self.next_button:
                self.next_button.update(dt)
            if self.back_button:
                self.back_button.update(dt)

    def draw(self, screen):
        if self.background:
            screen.blit(self.background, (0, 0))

        title_text = self.font_large.render("Hero Collection", True, COLOR_GOLD)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title_text, title_rect)

        self._draw_hero_slots(screen)

        if self.page_display:
            self.page_display.draw(screen)

        if self.prev_button:
            self.prev_button.draw(screen)
        if self.next_button:
            self.next_button.draw(screen)
        if self.back_button:
            self.back_button.draw(screen)

        if self.selected_hero:
            self._draw_detail_panel(screen)

    def _draw_hero_slots(self, screen):
        for rect, hero_id, is_owned in self.hero_slots:
            slot_color = (60, 50, 40) if is_owned else (30, 25, 20)
            pygame.draw.rect(screen, slot_color, rect)
            pygame.draw.rect(screen, (100, 80, 60), rect, 2)

            hero = get_hero(hero_id)
            if not hero:
                continue

            if is_owned:
                try:
                    portrait = self.assets.load_image(hero.portrait_path, (rect.width - 10, rect.height - 30))
                    portrait_rect = portrait.get_rect(center=(rect.centerx, rect.centery - 10))
                    screen.blit(portrait, portrait_rect)
                except Exception as e:
                    print(f"Warning: Could not load portrait for hero {hero_id}: {e}")
                    pygame.draw.circle(screen, (100, 100, 100), rect.center, 40)

                name_text = self.font_small.render(hero.name[:12], True, COLOR_WHITE)
                name_rect = name_text.get_rect(center=(rect.centerx, rect.bottom - 10))
                screen.blit(name_text, name_rect)
            else:
                lock_text = self.font_large.render("?", True, (80, 70, 60))
                lock_rect = lock_text.get_rect(center=rect.center)
                screen.blit(lock_text, lock_rect)

                locked_text = self.font_small.render("Locked", True, (100, 90, 80))
                locked_rect = locked_text.get_rect(center=(rect.centerx, rect.bottom - 10))
                screen.blit(locked_text, locked_rect)

    def _draw_detail_panel(self, screen):
        if not self.selected_hero or not self.detail_panel_rect:
            return

        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (50, 40, 30), self.detail_panel_rect)
        pygame.draw.rect(screen, COLOR_GOLD, self.detail_panel_rect, 3)

        portrait_size = 200
        portrait_y = self.detail_panel_rect.top + 20
        try:
            portrait = self.assets.load_image(self.selected_hero.portrait_path, (portrait_size, portrait_size))
            portrait_rect = portrait.get_rect(center=(self.detail_panel_rect.centerx, portrait_y + portrait_size // 2))
            screen.blit(portrait, portrait_rect)
        except Exception as e:
            print(f"Warning: Could not load portrait: {e}")

        name_y = portrait_y + portrait_size + 20
        name_text = self.font_large.render(self.selected_hero.name, True, COLOR_GOLD)
        name_rect = name_text.get_rect(center=(self.detail_panel_rect.centerx, name_y))
        screen.blit(name_text, name_rect)

        rarity_y = name_y + 40
        rarity_color = self._get_rarity_color(self.selected_hero.rarity)
        rarity_text = self.font_normal.render(f"Rarity: {self.selected_hero.rarity.upper()}", True, rarity_color)
        rarity_rect = rarity_text.get_rect(center=(self.detail_panel_rect.centerx, rarity_y))
        screen.blit(rarity_text, rarity_rect)

        power_y = rarity_y + 35
        power_text = self.font_normal.render(f"Power: {self.selected_hero.power}", True, COLOR_WHITE)
        power_rect = power_text.get_rect(center=(self.detail_panel_rect.centerx, power_y))
        screen.blit(power_text, power_rect)

        stats_y = power_y + 50
        stats_title = self.font_normal.render("Stats:", True, COLOR_GOLD)
        stats_title_rect = stats_title.get_rect(center=(self.detail_panel_rect.centerx, stats_y))
        screen.blit(stats_title, stats_title_rect)

        stat_y = stats_y + 35
        stat_spacing = 30
        for stat_name, stat_value in self.selected_hero.stats.items():
            stat_text = self.font_small.render(f"{stat_name.upper()}: {stat_value}", True, COLOR_WHITE)
            stat_rect = stat_text.get_rect(center=(self.detail_panel_rect.centerx, stat_y))
            screen.blit(stat_text, stat_rect)
            stat_y += stat_spacing

        if self.detail_close_button:
            self.detail_close_button.draw(screen)

    def _get_rarity_color(self, rarity: str) -> tuple:
        rarity_colors = {
            'rare': (100, 150, 255),
            'legendary': (200, 100, 255),
            'extreme': (255, 200, 50),
        }
        return rarity_colors.get(rarity, COLOR_WHITE)

    def exit(self):
        self.selected_hero = None
