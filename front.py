# front.py

#import
import pygame, sys
import pygame.mouse
import pygame.image
import pygame.font
import json
pygame.init()

#load and setup
with open("data.json") as f:
    data = json.load(f)
    width = data["settings"]["width"]
    height = data["settings"]["height"]
fonts = pygame.font.SysFont("Monocraft", 18)
screen = pygame.display.set_mode((width, height))
frontbackground = pygame.image.load("assets/backgrounds/town_2.png").convert()
run = True
clock = pygame.time.Clock()

#text
class TextButton:
    def __init__(self, baseimage, center, on_click=None, scale=2.0, use_mask=True):
        base = pygame.image.load(baseimage).convert_alpha()
        if scale != 2.0:
            w,h = base.get_size()
            base = pygame.transform.smoothscale(base, (int(w*scale), int(h*scale)))
        self.normal = base
        self.hover = effect(base, (230,240,245,255))
        self.pressed = effect(base, (200,200,200,255))
        self.image = self.normal
        self.rect = self.image.get_rect(center=center)
        self.on_click = on_click
        self._held = False
        self.use_mask = use_mask
        self.mask = pygame.mask.from_surface(self.image) if use_mask else None
    def hit(self, pos):
        if not self.rect.collidepoint(pos):
            return False
        if not self.use_mask:
            return True
        lx, ly = pos[0]-self.rect.x, pos[1]-self.rect.y
        return bool(self.mask.get_at((lx, ly)))
    def update(self, events):
        mpos  = pygame.mouse.get_pos()
        mdown = pygame.mouse.get_pressed()[0]
        over  = self.hit(mpos)

        if over and mdown:
            self.image = self.pressed; self._held = True
        elif over:
            self.image = self.hover
            for e in events:
                if e.type == pygame.MOUSEBUTTONUP and e.button == 1 and self._held:
                    self._held = False
                    if self.on_click: self.on_click()
        else:
            self.image = self.normal; self._held = False

    def draw(self, surf):
        shadow = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0,0,0,60),(0, self.rect.height*0.75, self.rect.width, self.rect.height*0.5))
        surf.blit(shadow, (self.rect.x, self.rect.y))
        surf.blit(self.image, self.rect)
def start_game(): print("main")
def open_settings(): print("settings")
def quit_game(): pygame.quit(); sys.exit()
def effect(src: pygame.Surface, mul=(230,230,230,255)):
    img = src.copy()
    img.fill(mul, special_flags=pygame.BLEND_RGBA_MULT)
    return img

#botton
BASE = "assets/ui/12.png"
BUTTON_SCALE = 1.2
labels = ["START", "SETTINGS", "QUIT"]

centers = [
    (width//2, height//2 - 80),
    (width//2, height//2),
    (width//2, height//2 + 80)
]
handlers = [start_game, open_settings, quit_game]
buttons = []
for c, cb in zip(centers, handlers):
    buttons.append(TextButton(BASE, center=c, on_click=cb, scale=BUTTON_SCALE, use_mask=True))
WHITE = (255,255,255)

# running
while run:
    events = pygame.event.get()
    for e in events:
        if e.type == pygame.QUIT:
            run = False

    for b in buttons:
        b.update(events)

    screen.blit(frontbackground, (0, 0))
    for i, b in enumerate(buttons):
        b.draw(screen)
        text = fonts.render(labels[i], True, WHITE)
        screen.blit(text, text.get_rect(center=b.rect.center))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
sys.exit()