import pygame
from src.screen.base_screen import BaseScreen
from src.screen.setting_screen import SettingScreen
from src.ui.button import Button

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.game_manager import GameManager

class LobbyScreen(BaseScreen):
    def __init__(self, manager: 'GameManager'):
        super().__init__(manager)

        self.setBackground('town1.png')
        self.statusButtons: list[Button] = []
        self.chestButtons: list[Button] = []

        self._setup_ui()

    def _setup_ui(self) -> None:
        self.statusButtons = [
            Button(
                x= 640,
                y= 70,
                image_name='status_background.png',
                text= '10000',
                font_size= 18
            ),
            Button(
                x= 510,
                y= 68,
                image_name='profile_button.png',
                callback= self._profileScreen,
            ),
            Button(
                x= 774,
                y= 68,
                image_name='redeem_button.png',
                callback= self._redeemCodeScreen,
            ),
            Button(
                x= 710,
                y= 70,
                image_name='coin_icon.png',
                callback= self._redeemCodeScreen,
            ),
            Button(
                x= 1210,
                y= 70,
                image_name='setting_icon.png',
                callback= self._settingScreen,
            )
        ]

        self.chestButtons = [
            Button(
                x= 440,
                y= 620,
                image_name= 'mystic_chest_background.png',
                text= 'Mystic Chest',
                font_size = 11,
                text_y= 668,
                callback= self._mysticChest
            ),
            Button(
                x= 640,
                y= 620,
                image_name= 'celestial_chest_background.png',
                text= 'Celestial Chest',
                font_size = 11,
                text_y= 668,
                callback= self._celestialChest
            ),
            Button(
                x= 840,
                y= 620,
                image_name= 'collection_background.png',
                text= 'COLLECTION',
                font_size = 11,
                text_y= 668,
                callback= self._collectionScreen
            )
        ]

    def render(self, screen):
        screen.blit(self.background, (0,0))
        self.update_transition(screen)

        for button in self.statusButtons:
            button.render(screen)
        
        for button in self.chestButtons:
            button.render(screen)

    def handleEvents(self, events: list[pygame.event.Event]) -> None:
        for event in events:
            for button in self.statusButtons:
                button.handleEvent(event)
            
            for button in self.chestButtons:
                button.handleEvent(event)

    def _redeemCodeScreen(self):
        print('redeem Code')

    def _profileScreen(self):
        print('profile')

    def _settingScreen(self):
        self.manager.screenManager.changeScreen('setting')
        print('setting')
    
    def _mysticChest(self):
        print('mystic chest')

    def _celestialChest(self):
        print('celestial chest')

    def _collectionScreen(self):
        print('Collection')
