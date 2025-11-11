from abc import ABC, abstractmethod
import pygame


class GameState(ABC):
    def __init__(self, game):
        self.game = game
        self.assets = None
    
    @abstractmethod
    def handle_event(self, event):
        pass
    
    @abstractmethod
    def update(self, dt):
        pass
    
    @abstractmethod
    def draw(self, screen):
        pass
    
    def enter(self):
        pass
    
    def exit(self):
        pass
