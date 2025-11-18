import pygame
import sys
from src.core.game_manager import GameManager

def main():
    game_manager = None

    pygame.init()
    game_manager = GameManager()
    game_manager.run()

    # try:
    #     pygame.init()

    #     print("=" * 50)
    #     print("Gacha Legends - Game Starting...")
    #     print("=" * 50) 

    #     game_manager = GameManager()
    #     game_manager.run()
    
    # except Exception as e:
    #     print("\n" + "=" * 50)
    #     print("ERROR: An unexpected error occurred!")
    #     print("=" * 50)
    #     print(f"Error Type: {type(e).__name__}")
    #     print(f"Error Message: {str(e)}")
    #     print("\nPlease report this error if it persists.")
    
    # finally:
    #     if game_manager:
    #         try:
    #             game_manager.quit_game()
    #         except:
    #             pass
        
    #     pygame.quit()
    #     print("\nGame closed. Thank you for playing!\n")
    #     sys.exit(0)

if __name__ == '__main__':
    main()