import pygame
from src.screen.base_screen import BaseScreen
from src.ui.text_display import TextDisplay
from src.ui.button import Button

class SettingScreen(BaseScreen):
    def __init__(self, manager):
        super().__init__(manager)
        self.setBackground('town2.png')

        self._setup_ui()

        self.dragging = False
    
    def _setup_ui(self):
        self.sliderButton_x = 640
        self.sliderButton_y = 350

        self.sliderBar = Button(
                x= 640,
                y= 350,
                image_name= 'slider_bar.png'
        )
        self.sliderButton = Button(
                x= self.sliderButton_x,
                y= self.sliderButton_y,
                image_name= 'slider_button.png'
        )

        self.testtext = TextDisplay(
            x= 640,
            y= 230,
            text= 'SETTING',
            font_size= 40
        )

    def handleEvents(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.sliderButton.imageRect.collidepoint(event.pos):
                    self.dragging = True

            if event.type == pygame.MOUSEBUTTONUP:
                self.dragging = False

            if event.type == pygame.MOUSEMOTION and self.dragging:
                mouse_x, mouse_y = event.pos

                new_x = mouse_x - self.sliderButton.imageRect.width // 2

                new_x = max(610, min(new_x, 750))

                self.sliderButton.imageRect.x = new_x

                slider_value = (new_x - 610) / (750 - 610)
                print(f"value: {slider_value:.2f}")

    def render(self, screen):
        screen.blit(self.background, (0,0))

        self.testtext.render(screen)
        self.sliderBar.render(screen)
        self.sliderButton.render(screen)