"""คลาสหลักของเกมพร้อม game loop"""

import pygame
import sys
from src.core.state_manager import StateManager
from src.core.config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE, GAME_LOGO_PATH


class Game:
    """คลาสหลักของเกมที่จัดการ game loop และ state"""

    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(GAME_TITLE)
        self.logo = pygame.image.load(GAME_LOGO_PATH)
        pygame.display.set_icon(self.logo)

        self.clock = pygame.time.Clock()
        self.running = False
        self.state_manager = StateManager()
        self.current_player_slot = None  # เก็บ slot ของผู้เล่นปัจจุบัน (1 หรือ 2)
        
        # ระบบเพลง
        self.music_loaded = False
        # ไม่โหลดเพลงตอน init แล้ว จะโหลดตอนเลือกผู้เล่น

    def change_state(self, state_name):
        """พฤติกรรมเดิม: เฟดออก -> เปลี่ยน -> เฟดเข้า"""
        self.state_manager.change_state(state_name)

    # เพิ่ม: เปลี่ยนฉากก่อน แล้วเฟดเข้า
    def change_state_then_fade_in(self, state_name, duration=0.3):
        self.state_manager.change_state_then_fade_in(state_name, duration=duration)

    def quit(self):
        self.running = False

    def save_game(self, filepath=None):
        """บันทึกข้อมูลผู้เล่นปัจจุบัน"""
        from src.utils import player
        
        if hasattr(self, 'player_data') and hasattr(self, 'current_player_slot'):
            return player.save_player_data(self.player_data, self.current_player_slot)
        return False
    
    def load_player_data(self, player_slot):
        """โหลดข้อมูลผู้เล่นตาม slot (1 หรือ 2)"""
        from src.utils import player
        
        self.current_player_slot = player_slot
        
        # โหลดข้อมูลผู้เล่น (เป็น dict)
        self.player_data: dict[str, any] = player.load_player_data(player_slot)
        
        print(f"Load Player {player_slot} Successfully")
        
        # โหลดและเล่นเพลง (ครั้งแรกหลังจากเลือกผู้เล่น)
        if not self.music_loaded:
            self._load_music()
        
        # อัปเดต states ที่ใช้ player_data
        self._update_player_states()
    
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
                    volume = self.player_data['settings'].get('volume', 50) / 100.0
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
    
    def _update_player_states(self):
        """อัปเดต states ที่ใช้ player_data หลังจากโหลดข้อมูลผู้เล่นใหม่"""
        if not hasattr(self, 'player_data'):
            return
        
        # อัปเดต volume ของเพลงตามค่าที่บันทึกไว้
        volume = self.player_data['settings'].get('volume', 50) / 100.0
        self.set_music_volume(volume)
        
        # เริ่มเพลงใหม่ถ้ายังไม่เล่น
        if self.music_loaded and not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
        
        # สร้าง/อัปเดต states ที่ใช้ player_data
        try:
            from src.screen.main_lobby_state import MainLobbyState
            from src.screen.profile_state import ProfileState
            from src.screen.book_state import BookState
            from src.screen.mystic_chest_state import MysticChestState
            from src.screen.celestial_chest_state import CelestialChestState
            
            # สร้าง states ใหม่ด้วย player_data ที่อัปเดต
            self.state_manager.add_state('main_lobby', MainLobbyState(self, self.player_data))
            self.state_manager.add_state('profile', ProfileState(self, self.player_data))
            self.state_manager.add_state('book', BookState(self, self.player_data))
            self.state_manager.add_state('mystic_chest', MysticChestState(self, self.player_data))
            self.state_manager.add_state('celestial_chest', CelestialChestState(self, self.player_data))
            
        except Exception as e:
            print(f"Error states: {e}")

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
