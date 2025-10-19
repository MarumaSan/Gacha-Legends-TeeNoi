"""คลาสหลักของเกมพร้อม game loop"""

import pygame
import sys
from game.state_manager import StateManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE


class Game:
    """คลาสหลักของเกมที่จัดการ game loop และ state"""

    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(GAME_TITLE)

        self.clock = pygame.time.Clock()
        self.running = False
        self.state_manager = StateManager()

    def change_state(self, state_name):
        """พฤติกรรมเดิม: เฟดออก -> เปลี่ยน -> เฟดเข้า"""
        self.state_manager.change_state(state_name)

    # เพิ่ม: เปลี่ยนฉากก่อน แล้วเฟดเข้า
    def change_state_then_fade_in(self, state_name, duration=0.3):
        self.state_manager.change_state_then_fade_in(state_name, duration=duration)

    def quit(self):
        self.running = False

    def save_game(self, filepath="save_data.json"):
        if hasattr(self, 'player_data'):
            return self.player_data.save_to_file(filepath)
        return False

    def run(self):
        self.running = True
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                else:
                    self.state_manager.handle_event(event)

            self.state_manager.update(dt)
            self.state_manager.draw(self.screen)
            pygame.display.flip()

        pygame.quit()
        sys.exit()
