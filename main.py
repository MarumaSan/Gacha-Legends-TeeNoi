"""Hero Gacha Game - จุดเริ่มต้นของเกม"""

from game import Game
from game.states import LoadingState, MainLobbyState, SettingsState, ProfileState, GachaState, BookState
from game.data.player_data import PlayerData


def main():
    """ฟังก์ชันหลักสำหรับรันเกม"""
    # สร้างและรันเกม
    game = Game()
    
    # สร้างข้อมูลผู้เล่น (ใช้ร่วมกันทุก state)
    player_data = PlayerData()
    
    # พยายามโหลดข้อมูลที่บันทึกไว้
    save_file = "save_data.json"
    if player_data.load_from_file(save_file):
        print(f"โหลดข้อมูลเกมจาก {save_file} สำเร็จ")
    else:
        print("เริ่มเกมใหม่ด้วยข้อมูลเริ่มต้น")
    
    game.player_data = player_data  # เก็บ reference ไว้ใช้งานง่าย
    
    # เพิ่ม states ทั้งหมด
    game.state_manager.add_state('loading', LoadingState(game))
    game.state_manager.add_state('main_lobby', MainLobbyState(game, player_data))
    game.state_manager.add_state('settings', SettingsState(game))
    game.state_manager.add_state('profile', ProfileState(game, player_data))
    game.state_manager.add_state('gacha', GachaState(game, player_data))
    game.state_manager.add_state('book', BookState(game, player_data))
    
    # เริ่มที่หน้า loading
    game.change_state('loading')
    
    # รันเกม
    try:
        game.run()
    finally:
        # บันทึกข้อมูลผู้เล่นเมื่อปิดเกม
        if player_data.save_to_file(save_file):
            print(f"บันทึกข้อมูลเกมไปที่ {save_file} สำเร็จ")
        else:
            print("บันทึกข้อมูลเกมไม่สำเร็จ")


if __name__ == "__main__":
    main()
