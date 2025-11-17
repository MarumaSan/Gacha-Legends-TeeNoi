import pygame
from typing import Callable
from src.utils.constants import PATH_FONTS, COLOR_WHITE

class InputBox:
    def __init__(
            self,
            x,
            y,
            w,
            h,
            text: str = '',
            default_text: str = '',
            size: int = 32,
            color = COLOR_WHITE,
    ):  
        self.rect = pygame.Rect(x, y, w, h)

        self.border_color_inactive = pygame.Color('gray20')
        self.border_color_active   = pygame.Color('purple')
        self.color = color
        self.border_color = self.border_color_inactive

        self.text = text
        self.submit_text = text    
        self.default_text = default_text  
        self.default_color = pygame.Color(150, 150, 150)

        self.size = size
        self.font = pygame.font.Font(PATH_FONTS + 'Monocraft.ttf', self.size)

        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = True
                self.border_color = self.border_color_active
            else:
                self.active = False
                self.border_color = self.border_color_inactive

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.submit_text = self.text
                self.text = ''
                return "SUBMIT"

            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]

            else:
                if event.unicode.isalnum():
                    self.text += event.unicode.upper()

        return None

    def draw(self, screen):
        if self.active:
            display_text = self.text
            color = self.color
        else:
            if self.text:
                display_text = self.text
                color = self.color
            else:
                display_text = self.default_text
                color = self.default_color

        txt_surface = self.font.render(display_text, True, color)
        text_rect = txt_surface.get_rect(center=self.rect.center)

        screen.blit(txt_surface, text_rect)

        # pygame.draw.rect(screen, self.border_color, self.rect, 2)
