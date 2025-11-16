"""Hero Gacha Game - จุดเริ่มต้นของเกม"""

import pygame
import sys

# Import ทุกอย่างที่ต้องใช้
from src.core.game import Game
from src.screen.loading_state import LoadingState
from src.screen.main_lobby_state import MainLobbyState
from src.screen.settings_state import SettingsState
from src.screen.profile_state import ProfileState
from src.screen.book_state import BookState
from src.screen.add_code_state import AddCodeState
from src.screen.mystic_chest_state import MysticChestState
from src.screen.celestial_chest_state import CelestialChestState
from src.screen.leaderboard_state import LeaderboardState
from src.screen.mystic_info_state import MysticInfoState
from src.screen.celestial_info_state import CelestialInfoState
from src.screen.how_to_play_state import HowToPlayState
from src.screen.battle_state import BattleState


# ตัวแปรสำหรับเก็บข้อมูลเกม
game = None
current_player = None  # 1 หรือ 2


def setup_game():
    """ตั้งค่าเกมครั้งแรก"""
    global game
    
    # สร้างเกม
    game = Game()
    
    # เพิ่มหน้าจอต่างๆ (states)
    game.state_manager.add_state('loading', LoadingState(game))
    game.state_manager.add_state('settings', SettingsState(game))
    game.state_manager.add_state('add_code', AddCodeState(game))
    game.state_manager.add_state('leaderboard', LeaderboardState(game))
    game.state_manager.add_state('mystic_info', MysticInfoState(game))
    game.state_manager.add_state('celestial_info', CelestialInfoState(game))
    game.state_manager.add_state('how_to_play', HowToPlayState(game))
    game.state_manager.add_state('battle', BattleState(game))
    
    # เริ่มที่หน้า loading (เลือกผู้เล่น)
    game.change_state('loading')


def save_player_data():
    """บันทึกข้อมูลผู้เล่น"""
    global game, current_player
    
    if game and hasattr(game, 'current_player_slot') and game.current_player_slot:
        if game.save_game():
            print(f"✓ บันทึกข้อมูล Player {game.current_player_slot} สำเร็จ")
        else:
            print("✗ บันทึกข้อมูลไม่สำเร็จ")


def main():
    """ฟังก์ชันหลัก - เริ่มเกม"""
    
    # ตั้งค่าเกม
    setup_game()
    
    # รันเกม
    try:
        game.run()
    except KeyboardInterrupt:
        print("\nกำลังปิดเกม...")
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")
    finally:
        # บันทึกข้อมูลก่อนปิด
        save_player_data()
        print("ปิดเกมแล้ว")


# เริ่มเกมเมื่อรันไฟล์นี้
if __name__ == "__main__":
    main()

