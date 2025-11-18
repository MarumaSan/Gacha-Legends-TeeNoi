import pygame
from src.ui.button import Button
from src.ui.text_display import TextDisplay
from src.ui.image import Image
from src.screen.base_screen import BaseScreen
from src.utils.constants import COLOR_YELLOW
from src.ui.input_box import InputBox
from src.utils.codes import REDEEM_CODES

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game_manager import GameManager

class RedeemScreen(BaseScreen):
    def __init__(self, manager: 'GameManager'):
        super().__init__(manager)

        self.setBackground('summon2.png')

        self.buttons: list[Button] = []
        self.textDisplays: list[TextDisplay] = []
        self.images: list[Image] = []

        self._setup_ui()

    def _setup_ui(self) -> None:
        self.buttons = [
            Button(
                x= self.center_x,
                y= 660,
                image_name= 'wood1_background.png',
                text= 'RETURN TO LOBBY',
                font_size= 14,
                callback= self.backToLobby
            )
        ]

        self.textDisplays = [
            TextDisplay(
                x= self.center_x,
                y= 150,
                text= 'SETTING',
                size= 60
            ),
            TextDisplay(
                x= self.center_x,
                y= 250,
                text= 'MONEY',
                size= 18,
                color= COLOR_YELLOW
            ),
            TextDisplay(
                x= self.center_x,
                y= 500,
                text= '+ MONEY',
                size= 18,
                color= COLOR_YELLOW,
                enable= False
            )
        ]

        self.images = [
            Image(
                x= self.center_x,
                y= self.center_y,
                image_name= 'wood2_background.png'
            )
        ]

        self.input_box = InputBox(
            x= self.center_x - 175,
            y= self.center_y - 25,
            w= 350,
            h= 50,
            size= 18,
            default_text= 'CODE'
        )

        self.redeem_code = REDEEM_CODES.keys()

    def render(self, screen):
        screen.blit(self.background, (0,0))

        for button in self.buttons:
            button.render(screen)

        for image in self.images:
            image.render(screen)

        for text in self.textDisplays:
            text.render(screen)

        self.input_box.draw(screen)

        self.update_transition(screen)
    
    def update(self):
        pass

    def handleEvents(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            if self.input_box.handle_event(event) == "SUBMIT":
                if self.input_box.submit_text in self.redeem_code :
                    if self.manager.player_data.use_code(self.input_box.submit_text, REDEEM_CODES[self.input_box.submit_text]):
                        self.textDisplays[1].setText(f'COINS : {self.manager.player_data.coins}')
                        self.textDisplays[2].setEnable(True)
                        self.textDisplays[2].setText(f'+ {REDEEM_CODES[self.input_box.submit_text]}')
                        self.manager.save_systems[self.manager.current_player_id].save_game(self.manager.player_data)
                continue

            if self._dispatch_event(self.buttons, event):
                continue
                

    def start_screen(self):
        self.textDisplays[1].setText(f'COINS : {self.manager.player_data.coins}')
        
        self.textDisplays[2].setEnable(True)

    def backToLobby(self):
        self.manager.screenManager.changeScreen('lobby')

    def redeem(self):
        pass
