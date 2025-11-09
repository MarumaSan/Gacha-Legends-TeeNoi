import pygame
import sys
from src.core.game_manager import GameManager

def main():
    game_manager = GameManager()
    game_manager.run()

if __name__ == '__main__':
    main()