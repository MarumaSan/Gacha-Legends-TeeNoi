# ตั้งค่าหน้าจอ
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
GAME_TITLE = "Gacha Legends: Tee Noi Edition"

# สี
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GOLD = (255, 215, 0)
COLOR_SILVER = (192, 192, 192)
COLOR_BRONZE = (205, 127, 50)

# สมดุลเกม
STARTING_COINS = 1000  # เหรียญเริ่มต้น
DAILY_BONUS = 100      # โบนัสรายวัน
TOTAL_HEROES = 21      # จำนวนฮีโร่ทั้งหมด

# ราคาสุ่ม
SUMMON_COSTS = {
    'mystic_x1': 100,
    'mystic_x10': 900,
    'celestial_x1': 150,
    'celestial_x10': 1350
}

# อัตราความหายาก
RARITY_RATES = {
    'rare': 0.70,   # 70% 
    'epic': 0.25,   # 25%
    'legendary': 0.04,  # 4%
    'extreme': 0.01  # 1%  
}

# path ของ assets
ASSET_PATHS = {
    'backgrounds': {
        'loading': 'assets/backgrounds/town_1.png',
        'lobby': 'assets/backgrounds/town_2.png',
        'summon_1': 'assets/backgrounds/summon_1.png',
        'summon_2': 'assets/backgrounds/summon_2.png',
        'book': 'assets/backgrounds/book.png'
    },
    'portraits': {
        f'hero{i}': f'assets/portraits/hero{i}.png' 
        for i in range(1, 22)
    },
    'cards': {
        'front': {f'hero{i}': f'assets/cards/front/hero{i}.png' for i in range(1, 22)},
        'back': {
            'rare': 'assets/cards/back/rare.PNG',
            'legendary': 'assets/cards/back/legendary.PNG',
            'extreme': 'assets/cards/back/extreme.PNG'
        }
    },
    'ui': {
        f'ui{i}': f'assets/ui/{i}.png' 
        for i in range(1, 13)
    },
    'fonts': {
        'monocraft': 'assets/fonts/Monocraft.ttf'
    }
}

FONTS = {
    'title': ('assets/fonts/Monocraft.ttf', 48),
    'normal': ('assets/fonts/Monocraft.ttf', 24),
    'small': ('assets/fonts/Monocraft.ttf', 16)
}
