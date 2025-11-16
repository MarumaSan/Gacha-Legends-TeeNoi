import pygame
from src.core.game_state import GameState
from src.utils import assets
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT


def _color_effect(src: pygame.Surface, mul=(230, 230, 230, 255)) -> pygame.Surface:
    img = src.copy()
    img.fill(mul, special_flags=pygame.BLEND_RGBA_MULT)
    return img


class _ImageButton:
    def __init__(self, base_img: pygame.Surface, center, on_click=None, scale=1.2, use_mask=True, text="", font=None):
        if scale != 1.0:
            w, h = base_img.get_size()
            base_img = pygame.transform.smoothscale(base_img, (int(w * scale), int(h * scale)))

        self.normal = base_img
        self.hover = _color_effect(base_img, (230, 240, 245, 255))
        self.down = _color_effect(base_img, (200, 200, 200, 255))

        self.image = self.normal
        self.rect = self.image.get_rect(center=center)

        self.on_click = on_click
        self._held = False
        self._over = False

        self.use_mask = use_mask
        self.mask = pygame.mask.from_surface(self.image) if use_mask else None

        self.text = text
        self.font = font
        self.text_color = (255, 255, 255)

    def _hit(self, pos):
        if not self.rect.collidepoint(pos):
            return False
        if not self.use_mask:
            return True
        lx, ly = pos[0] - self.rect.x, pos[1] - self.rect.y
        return bool(self.mask.get_at((lx, ly)))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self._hit(event.pos):
                self._held = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self._held and self._hit(event.pos):
                if self.on_click:
                    self.on_click()
            self._held = False

    def update(self, dt):
        mpos = pygame.mouse.get_pos()
        self._over = self._hit(mpos)

        if self._over and self._held:
            self.image = self.down
        elif self._over:
            self.image = self.hover
        else:
            self.image = self.normal

    def draw(self, surf):
        shadow = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 60),
                            (0, int(self.rect.height * 0.75), self.rect.width, int(self.rect.height * 0.5)))
        surf.blit(shadow, (self.rect.x, self.rect.y))
        surf.blit(self.image, self.rect)

        if self.text and self.font:
            label = self.font.render(self.text, True, self.text_color)
            surf.blit(label, label.get_rect(center=self.rect.center))


class LoadingState(GameState):
    """Loading screen state with player selection (PLAYER 1, PLAYER 2, QUIT)"""
    def __init__(self, game):
        super().__init__(game)
        self.background = None
        self.font = None

        self.btn_player1 = None
        self.btn_player2 = None
        self.btn_battle = None
        self.btn_quit = None
        self.btn_question = None

        self.BUTTON_BASE_PATH = 'assets/ui/12.png'
        self.BUTTON_SCALE = 1.2

    def enter(self):
        # หยุดเพลงในหน้า loading
        pygame.mixer.music.stop()
        
        try:
            self.background = assets.load_image('assets/backgrounds/town_2.png').convert()
        except Exception as e:
            print(f"โหลดพื้นหลังไม่ได้: {e}")
            self.background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.background.fill((50, 50, 100))

        try:
            self.font = assets.load_font('assets/fonts/Monocraft.ttf', 15)
        except Exception as e:
            print(f"โหลดฟอนต์ไม่ได้: {e}")
            self.font = pygame.font.Font(None, 15)

        try:
            base_img = assets.load_image(self.BUTTON_BASE_PATH).convert_alpha()
        except Exception as e:
            print(f"โหลดภาพปุ่มไม่ได้: {e}")
            base_img = pygame.Surface((220, 70), pygame.SRCALPHA)
            base_img.fill((60, 60, 90, 255))
            pygame.draw.rect(base_img, (255, 255, 255, 40), base_img.get_rect(), border_radius=16)

        centers = [
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40),
            (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120),
        ]

        self.btn_player1 = _ImageButton(
            base_img, centers[0], on_click=self.on_player1_click,
            scale=self.BUTTON_SCALE, use_mask=True, text="PLAYER 1", font=self.font
        )
        self.btn_player2 = _ImageButton(
            base_img, centers[1], on_click=self.on_player2_click,
            scale=self.BUTTON_SCALE, use_mask=True, text="PLAYER 2", font=self.font
        )
        self.btn_battle = _ImageButton(
            base_img, centers[2], on_click=self.on_battle_click,
            scale=self.BUTTON_SCALE, use_mask=True, text="BATTLE", font=self.font
        )
        self.btn_quit = _ImageButton(
            base_img, centers[3], on_click=self.on_exit_click,
            scale=self.BUTTON_SCALE, use_mask=True, text="QUIT", font=self.font
        )
        
        # โหลดรูปปุ่ม question
        try:
            question_img = assets.load_image('assets/ui/question.png', (50, 50))
        except Exception as e:
            print(f"Warning: Could not load question image: {e}")
            question_img = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.circle(question_img, (255, 255, 255), (25, 25), 25)
            font = pygame.font.Font(None, 40)
            text = font.render("?", True, (0, 0, 0))
            question_img.blit(text, (15, 5))
        
        # ปุ่ม Question (มุมขวาบน)
        self.btn_question = _ImageButton(
            question_img,
            center=(SCREEN_WIDTH - 40, 40),
            on_click=self.on_question_click,
            scale=1.0,
            use_mask=False
        )

    def on_player1_click(self):
        if getattr(self.game.state_manager, "transitioning", False):
            return
        print("เลือก PLAYER 1")
        # โหลดข้อมูลผู้เล่น 1
        self.game.load_player_data(1)
        # เข้าเกม
        if hasattr(self.game, "change_state_then_fade_in"):
            self.game.change_state_then_fade_in('main_lobby', duration=0.6)
        else:
            self.game.change_state('main_lobby')

    def on_player2_click(self):
        if getattr(self.game.state_manager, "transitioning", False):
            return
        print("เลือก PLAYER 2")
        # โหลดข้อมูลผู้เล่น 2
        self.game.load_player_data(2)
        # เข้าเกม
        if hasattr(self.game, "change_state_then_fade_in"):
            self.game.change_state_then_fade_in('main_lobby', duration=0.6)
        else:
            self.game.change_state('main_lobby')

    def on_battle_click(self):
        if getattr(self.game.state_manager, "transitioning", False):
            return
        print("คลิกปุ่ม BATTLE")
        if hasattr(self.game, "change_state_then_fade_in"):
            self.game.change_state_then_fade_in('battle', duration=0.6)
        else:
            self.game.change_state('battle')
    
    def on_exit_click(self):
        if getattr(self.game.state_manager, "transitioning", False):
            return
        print("คลิกปุ่มออกเกม")
        self.game.quit()
    
    def on_question_click(self):
        if getattr(self.game.state_manager, "transitioning", False):
            return
        print("คลิกปุ่ม Question - ไปหน้า How to Play")
        self.game.change_state('how_to_play')

    def handle_event(self, event):
        if getattr(self.game.state_manager, "transitioning", False):
            return
        if self.btn_player1: self.btn_player1.handle_event(event)
        if self.btn_player2: self.btn_player2.handle_event(event)
        if self.btn_battle: self.btn_battle.handle_event(event)
        if self.btn_quit: self.btn_quit.handle_event(event)
        if self.btn_question: self.btn_question.handle_event(event)

    def update(self, dt):
        if getattr(self.game.state_manager, "transitioning", False):
            return
        if self.btn_player1: self.btn_player1.update(dt)
        if self.btn_player2: self.btn_player2.update(dt)
        if self.btn_battle: self.btn_battle.update(dt)
        if self.btn_quit: self.btn_quit.update(dt)
        if self.btn_question: self.btn_question.update(dt)

    def draw(self, screen: pygame.Surface):
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((30, 30, 60))
        if self.btn_player1: self.btn_player1.draw(screen)
        if self.btn_player2: self.btn_player2.draw(screen)
        if self.btn_battle: self.btn_battle.draw(screen)
        if self.btn_quit: self.btn_quit.draw(screen)
        if self.btn_question: self.btn_question.draw(screen)

    def exit(self):
        pass
