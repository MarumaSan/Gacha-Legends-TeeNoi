"""คลาสหลักของเกมพร้อม game loop"""

import pygame
import sys
from file_game.code.state_manager import StateManager
from file_game.code.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE


class Game:
    """คลาสหลักของเกมที่จัดการ game loop และ state"""

    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(GAME_TITLE)

        self.clock = pygame.time.Clock()
        self.running = False
        self.state_manager = StateManager()
        
        # ระบบเพลง
        self.music_loaded = False
        self._load_music()

    def change_state(self, state_name):
        """พฤติกรรมเดิม: เฟดออก -> เปลี่ยน -> เฟดเข้า"""
        self.state_manager.change_state(state_name)

    # เพิ่ม: เปลี่ยนฉากก่อน แล้วเฟดเข้า
    def change_state_then_fade_in(self, state_name, duration=0.3):
        self.state_manager.change_state_then_fade_in(state_name, duration=duration)

    def quit(self):
        self.running = False

    def save_game(self, filepath="file_game/json/save_data.json"):
        if hasattr(self, 'player_data'):
            return self.player_data.save_to_file(filepath)
        return False
    
    def _load_music(self):
        """โหลดและเล่นเพลงพื้นหลัง"""
        try:
            # โหลดเพลง bgm.mp3 จาก folder assets/song
            import os
            music_path = os.path.join("assets", "song", "bgm.mp3")
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                # ใช้ค่า volume จาก player_data ถ้ามี
                if hasattr(self, 'player_data'):
                    volume = self.player_data.settings.get('volume', 50) / 100.0
                else:
                    volume = 0.5
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1)  # เล่นวนซ้ำ
                self.music_loaded = True
                print(f"Music loaded: {music_path}")
            else:
                print(f"Music file not found: {music_path}")
                self.music_loaded = False
        except Exception as e:
            print(f"Could not load music: {e}")
            self.music_loaded = False
    
    def set_music_volume(self, volume):
        """ปรับความดังเพลง (0.0 - 1.0)"""
        if self.music_loaded:
            pygame.mixer.music.set_volume(volume)

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
