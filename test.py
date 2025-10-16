# front.py — complete fade + image-button + anti-misclick

import sys, json
from pathlib import Path
import pygame

pygame.init()

# ----------------------------
# Paths (robust to working dir)
# ----------------------------
BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data.json"
BG_MENU_PATH = BASE_DIR / "assets" / "backgrounds" / "town_2.png"
BG_GAME_PATH = BASE_DIR / "assets" / "backgrounds" / "game_bg.png"  # optional demo
BTN_IMAGE_PATH = BASE_DIR / "assets" / "ui" / "12.png"

# ----------------------------
# Load config
# ----------------------------
with open(DATA_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)
WIDTH  = int(data["settings"]["width"])
HEIGHT = int(data["settings"]["height"])

# ----------------------------
# Window / Fonts
# ----------------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tenoi Project • Front")

# พยายามใช้ Monocraft ถ้าไม่มี fallback ไป Arial
UI_FONT = pygame.font.SysFont("Monocraft", 18) or pygame.font.SysFont("Arial", 18)
TITLE_FONT = pygame.font.SysFont("Monocraft", 36) or pygame.font.SysFont("Arial", 36)

# ----------------------------
# Backgrounds
# ----------------------------
def load_bg(path: Path) -> pygame.Surface:
    surf = pygame.image.load(str(path)).convert()
    return pygame.transform.smoothscale(surf, (WIDTH, HEIGHT))

bg_current = load_bg(BG_MENU_PATH)  # เริ่มด้วยหน้ารายการ

# ----------------------------
# Fade state machine
# ----------------------------
FADE_OUT_MS = 600
FADE_IN_MS  = 600
phase = "idle"              # "idle" | "fade_out" | "switch" | "fade_in"
fade_t0 = 0
fade_overlay = pygame.Surface((WIDTH, HEIGHT))
fade_overlay.fill((0, 0, 0))

# ป้องกัน mis-click ตอนเพิ่งโฟกัสหน้าต่าง
INTERACT_DELAY_MS = 250
interactive_from = pygame.time.get_ticks() + INTERACT_DELAY_MS

# ----------------------------
# Utilities for button visuals
# ----------------------------
def tint_mult(src: pygame.Surface, rgba=(230,230,230,255)) -> pygame.Surface:
    """ทำให้มืดลง/หม่นลง (คูณสี)"""
    img = src.copy()
    img.fill(rgba, special_flags=pygame.BLEND_RGBA_MULT)
    return img

def tint_add(src: pygame.Surface, rgba=(90,90,90,0)) -> pygame.Surface:
    """ทำให้สว่างขึ้น (บวกสี)"""
    img = src.copy()
    img.fill(rgba, special_flags=pygame.BLEND_RGBA_ADD)
    return img

# ----------------------------
# Buttons
# ----------------------------
class TextButton:
    def __init__(self, base_image_path: Path, center, on_click=None, scale=1.0, use_mask=True):
        base = pygame.image.load(str(base_image_path)).convert_alpha()
        if scale != 1.0:
            w, h = base.get_size()
            base = pygame.transform.smoothscale(base, (int(w*scale), int(h*scale)))

        # สถานะภาพ
        self.normal  = base
        self.hover   = tint_add(base, (110,110,110,0))     # สว่างขึ้นชัด
        self.pressed = tint_mult(base, (190,190,190,255))  # มืดลงตอนกด
        self.image   = self.normal

        # เรขาคณิต / hit-test
        self.rect = self.image.get_rect(center=center)
        self.use_mask = use_mask
        self.mask = pygame.mask.from_surface(self.image) if use_mask else None

        # คลิก
        self.on_click = on_click
        self._held = False  # ต้อง DOWN บนปุ่มก่อน แล้วค่อย UP บนปุ่ม

    def _hit(self, pos) -> bool:
        if not self.rect.collidepoint(pos):
            return False
        if not self.use_mask:
            return True
        lx, ly = pos[0] - self.rect.x, pos[1] - self.rect.y
        return bool(self.mask.get_at((lx, ly)))

    def update(self, events, now, interactive_from_ms):
        mpos = pygame.mouse.get_pos()
        over = self._hit(mpos)

        # ภาพ hover โดยทั่วไป
        self.image = self.hover if over else self.normal

        # ยังไม่ให้โต้ตอบ จนกว่าจะพ้นดีเลย์เริ่มแรก (กันคลิกโฟกัสหน้าต่าง)
        if now < interactive_from_ms:
            self._held = False
            return

        # คลิกจริง: DOWN บนปุ่ม -> กดค้างเป็น pressed; ถ้า UP บนปุ่มด้วย -> click success
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and over:
                self._held = True
                self.image = self.pressed
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                if over and self._held:
                    self._held = False
                    if self.on_click and (phase == "idle"):
                        self.on_click()
                else:
                    self._held = False

    def draw(self, surf: pygame.Surface, label: str=None, font: pygame.font.Font=None, color=(255,255,255)):
        # เงานุ่ม
        shadow = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(
            shadow, (0,0,0,64),
            (0, self.rect.height*0.75, self.rect.width, self.rect.height*0.5)
        )
        surf.blit(shadow, self.rect.topleft)
        # ปุ่ม
        surf.blit(self.image, self.rect)
        # ข้อความกลางปุ่ม (ถ้าต้องการ)
        if label and font:
            ts = font.render(label, True, color)
            surf.blit(ts, ts.get_rect(center=self.rect.center))

# ----------------------------
# Scene switching handlers
# ----------------------------
def start_game():
    """เรียกเมื่อกดปุ่ม START → เริ่มเฟดออกจากเมนู"""
    global phase, fade_t0
    phase = "fade_out"
    fade_t0 = pygame.time.get_ticks()

def open_settings():
    print("settings")  # ใส่ลอจิกจริงภายหลังได้

def quit_game():
    pygame.quit()
    sys.exit()

def switch_to_game():
    """ช่วงสลับซีน (ระหว่างจอดำสนิท) — ใส่โหลดหน้าเกมจริงได้ตรงนี้"""
    global bg_current
    # เดโม: เปลี่ยนฉากพื้นหลัง (ถ้ามีไฟล์ game_bg.png)
    if BG_GAME_PATH.exists():
        bg_current = load_bg(BG_GAME_PATH)
    # ถ้ามีโมดูลเกมจริง ให้ import แล้วเรียก run(screen) ได้เลย:
    # import game
    # game.run(screen)

# ----------------------------
# Build buttons (centered stack)
# ----------------------------
BUTTON_SCALE = 1.2
labels = ["START", "SETTINGS", "QUIT"]
centers = [
    (WIDTH//2, HEIGHT//2 - 80),
    (WIDTH//2, HEIGHT//2),
    (WIDTH//2, HEIGHT//2 + 80),
]
handlers = [start_game, open_settings, quit_game]

buttons = [
    TextButton(BTN_IMAGE_PATH, center=c, on_click=cb, scale=BUTTON_SCALE, use_mask=True)
    for c, cb in zip(centers, handlers)
]

WHITE = (255,255,255)
clock = pygame.time.Clock()
running = True

# ----------------------------
# Main loop
# ----------------------------
while running:
    dt = clock.tick(60)
    now = pygame.time.get_ticks()
    events = pygame.event.get()

    for e in events:
        if e.type == pygame.QUIT:
            running = False

    # อัปเดตปุ่ม (พร้อมกัน miss-click guard)
    for b, label in zip(buttons, labels):
        b.update(events, now, interactive_from)

    # วาดฉากเมนู
    screen.blit(bg_current, (0, 0))
    for b, label in zip(buttons, labels):
        b.draw(screen, label=label, font=UI_FONT, color=WHITE)

    # Fade FSM: fade_out -> switch -> fade_in -> idle
    if phase == "fade_out":
        t = min(1.0, (now - fade_t0) / FADE_OUT_MS)
        fade_overlay.set_alpha(int(t * 255))      # ใส -> ดำ
        screen.blit(fade_overlay, (0, 0))
        if t >= 1.0:
            phase = "switch"

    elif phase == "switch":
        switch_to_game()
        phase = "fade_in"
        fade_t0 = now

    elif phase == "fade_in":
        t = min(1.0, (now - fade_t0) / FADE_IN_MS)
        fade_overlay.set_alpha(int((1.0 - t) * 255))  # ดำ -> ใส
        screen.blit(fade_overlay, (0, 0))
        if t >= 1.0:
            phase = "idle"

    pygame.display.flip()

pygame.quit()
sys.exit()