# Gacha Legends: Tee Noi Edition

เกม Gacha สะสมตัวละครแบบ turn-based พัฒนาด้วย Python และ Pygame

## 📋 สารบัญ
- [การติดตั้ง](#การติดตั้ง)
- [โครงสร้างโปรเจค](#โครงสร้างโปรเจค)
- [เส้นทางการทำงาน](#เส้นทางการทำงาน)
- [ระบบต่างๆ](#ระบบต่างๆ)

## 🚀 การติดตั้ง

```bash
# Clone โปรเจค
git clone <repository-url>
cd Gacha-Legends-TeeNoi

# สร้าง virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# หรือ
venv\Scripts\activate  # Windows

# ติดตั้ง dependencies
pip install pygame

# รันเกม
python main.py
```

## 📁 โครงสร้างโปรเจค

```
Gacha-Legends-TeeNoi/
├── main.py                 # จุดเริ่มต้นของเกม
├── src/
│   ├── core/              # ระบบหลักของเกม
│   │   ├── game.py        # คลาส Game หลัก (game loop)
│   │   ├── game_state.py  # Base class สำหรับ state ต่างๆ
│   │   ├── state_manager.py  # จัดการการเปลี่ยน state
│   │   └── config.py      # ค่าคงที่และการตั้งค่า
│   │
│   ├── screen/            # หน้าจอต่างๆ ของเกม
│   │   ├── loading_state.py        # หน้าเลือกผู้เล่น
│   │   ├── how_to_play_state.py    # หน้าวิธีเล่น (17 หน้า)
│   │   ├── main_lobby_state.py     # หน้าล็อบบี้หลัก
│   │   ├── profile_state.py        # หน้าโปรไฟล์และสถิติ
│   │   ├── book_state.py           # หน้าคอลเลคชั่น
│   │   ├── mystic_chest_state.py   # หน้าสุ่ม Mystic Chest
│   │   ├── celestial_chest_state.py # หน้าสุ่ม Celestial Chest
│   │   ├── mystic_info_state.py    # ข้อมูล Mystic Chest
│   │   ├── celestial_info_state.py # ข้อมูล Celestial Chest
│   │   ├── battle_state.py         # หน้าต่อสู้ระหว่างผู้เล่น
│   │   ├── settings_state.py       # หน้าตั้งค่า
│   │   ├── add_code_state.py       # หน้ากรอกโค้ด
│   │   └── leaderboard_state.py    # หน้าอันดับ
│   │
│   ├── data/              # ข้อมูลเกม
│   │   └── hero_data.py   # ข้อมูลตัวละคร
│   │
│   ├── ui/                # UI Components
│   │   ├── button.py      # ปุ่มทั่วไป
│   │   ├── slider.py      # แถบเลื่อน
│   │   ├── text_input.py  # ช่องกรอกข้อความ
│   │   ├── text_display.py # แสดงข้อความ
│   │   └── animation.py   # Animation (card flip)
│   │
│   └── utils/             # ฟังก์ชันช่วยเหลือ
│       ├── assets.py      # โหลดรูปภาพ/ฟอนต์
│       ├── player.py      # จัดการข้อมูลผู้เล่น
│       └── codes.py       # จัดการโค้ดแลกรางวัล
│
├── assets/                # ไฟล์ทรัพยากร
│   ├── backgrounds/       # รูปพื้นหลัง
│   ├── portraits/         # รูปตัวละคร
│   ├── cards/            # การ์ดตัวละคร
│   ├── ui/               # รูป UI
│   ├── fonts/            # ฟอนต์
│   ├── song/             # เพลงพื้นหลัง
│   └── How_to_play/      # รูปวิธีเล่น (1-17.png)
│
└── data/json/            # ข้อมูล JSON
    ├── codes.json        # โค้ดแลกรางวัล
    ├── save_data_player1.json  # ข้อมูล Player 1
    ├── save_data_player2.json  # ข้อมูล Player 2
    ├── used_codes_player1.json # โค้ดที่ใช้แล้ว Player 1
    └── used_codes_player2.json # โค้ดที่ใช้แล้ว Player 2
```

## 🎮 เส้นทางการทำงาน

### 1. การเริ่มต้นเกม (main.py)
```
main.py
  ↓
setup_game()
  ↓
สร้าง Game instance
  ↓
เพิ่ม states ทั้งหมด
  ↓
เริ่มที่ loading_state
  ↓
game.run() → game loop
```

### 2. Game Loop (src/core/game.py)
```
game.run()
  ↓
┌─────────────────────┐
│  ทุก frame:         │
│  1. handle_event()  │ ← รับ input จากผู้เล่น
│  2. update(dt)      │ ← อัปเดตสถานะเกม
│  3. draw(screen)    │ ← วาดหน้าจอ
│  4. display.flip()  │ ← แสดงผล
└─────────────────────┘
```

### 3. State Management (src/core/state_manager.py)
```
StateManager
  ↓
states = {
  'loading': LoadingState,
  'main_lobby': MainLobbyState,
  'mystic_chest': MysticChestState,
  ...
}
  ↓
change_state(name)
  ↓
current_state.exit()
  ↓
current_state = states[name]
  ↓
current_state.enter()
```

### 4. Flow การเล่นเกม

```
┌─────────────────┐
│ Loading Screen  │ ← เลือก Player 1, Player 2, BATTLE, QUIT
└────────┬────────┘
         │ กด ?
         ├──────────────┬──────────────┐
         │              │              │
         ↓              ↓              ↓
┌─────────────────┐  ┌──────────┐  ┌──────────────┐
│  How to Play    │  │ Settings │  │ Battle Mode  │
│  (17 หน้า)      │  │ - Volume │  │ (PvP)        │
└─────────────────┘  └──────────┘  └──────────────┘
         │
         ↓
┌─────────────────────────────────────┐
│      Main Lobby (หน้าหลัก)          │
│  - แสดงตัวละครที่มี (สูงสุด 3 ตัว)  │
│  - แสดงจำนวนเหรียญ                   │
│  - ปุ่ม Profile, Settings           │
└──────┬──────────────────────────────┘
       │
       ├─────────────┬─────────────┬──────────────┐
       │             │             │              │
       ↓             ↓             ↓              ↓
┌─────────────┐ ┌──────────┐ ┌─────────┐  ┌──────────┐
│ Mystic      │ │Celestial │ │Collection│  │ Profile  │
│ Chest       │ │ Chest    │ │ (Book)   │  │          │
│ - 100/900   │ │150/1350  │ │ 2 ตัว/   │  │- Stats   │
│   coins     │ │  coins   │ │  หน้า    │  │- Leader  │
│ - กด ?      │ │ - กด ?   │ │          │  │  board   │
│   ดู rate   │ │   ดู rate│ │          │  │ (Wins)   │
└─────────────┘ └──────────┘ └─────────┘  └──────────┘
       │             │
       ↓             ↓
┌─────────────┐ ┌──────────┐
│ Mystic Info │ │Celestial │
│ - Rare 79%  │ │   Info   │
│ - Epic 19%  │ │- Rare 70%│
│ - Leg. 1%   │ │- Epic 25%│
└─────────────┘ │- Leg. 4% │
                │- Ext. 1% │
                └──────────┘
```

### 5. ระบบสุ่มตัวละคร (Gacha System)

```
เลือกกล่อง (Mystic/Celestial)
  ↓
เลือกจำนวน (x1/x10)
  ↓
ตรวจสอบเหรียญ
  ↓
หักเหรียญ + แสดง animation "-XXX"
  ↓
สุ่ม rarity ตาม rate
  ↓
สุ่มตัวละครจาก pool
  ↓
STATE_REVEALING: แสดงการ์ดหลัง
  ↓
คลิกเปิดการ์ด → animation flip
  ↓
ถ้ามีตัวใหม่ → STATE_NEW_HERO
  ↓
STATE_RESULTS: แสดงผลทั้งหมด
  ↓
เลือก: SUMMON AGAIN หรือ RETURN TO LOBBY
```

### 6. ระบบบันทึกข้อมูล

```
Player Data (dict)
  ├── coins: int
  ├── owned_heroes: [hero_id, ...]
  ├── settings: {volume, sound_enabled}
  └── rank: int (แต้มชนะจาก Battle)

บันทึกที่:
  - data/json/save_data_player1.json
  - data/json/save_data_player2.json

บันทึกเมื่อ:
  - สุ่มตัวละคร
  - เปลี่ยนการตั้งค่า
  - ใช้โค้ด
  - จบการต่อสู้ (Battle)
  - ปิดเกม
```

## 🎯 ระบบต่างๆ

### ระบบเพลง (Audio System)
- โหลดเพลงจาก `assets/song/bgm.mp3`
- ปรับ volume ตาม settings ของผู้เล่น
- เล่นวนซ้ำตลอด

### ระบบโค้ด (Code System)
```
codes.json → โค้ดที่มีทั้งหมด
  ↓
ผู้เล่นกรอกโค้ด
  ↓
ตรวจสอบ:
  1. โค้ดมีอยู่จริงหรือไม่
  2. ใช้แล้วหรือยัง (used_codes_playerX.json)
  ↓
ถ้าถูกต้อง:
  - เพิ่มเหรียญ
  - บันทึกว่าใช้แล้ว
  - แสดง animation "+XXX"
```

### ระบบ Battle (PvP) - ชนะ 3 ใน 5 รอบ
```
เลือก BATTLE จากหน้า Loading
  ↓
กรอกจำนวนเงินเดิมพัน (ไม่เกินเงินที่น้อยกว่า)
  ↓
Player 1: สุ่มการ์ด 5 ใบ
  ├─ คลิกการ์ดเพื่อเลือกลำดับ (แสดงเลข 1-5)
  ├─ คลิกซ้ำเพื่อยกเลิก
  ├─ ปุ่ม CLEAR: ล้างลำดับทั้งหมด
  ├─ ปุ่ม CONFIRM: ยืนยัน (เมื่อเลือกครบ 5)
  └─ ปุ่ม BACK: กลับไปกรอกเงิน
  ↓
Player 2: สุ่มการ์ด 5 ใบ (เหมือน Player 1)
  ↓
ต่อสู้ทีละรอบ (5 รอบ หรือจนกว่าจะมีคนชนะ 3 รอบ)
  ├─ รอบที่ 1: การ์ดลำดับ 1 ของทั้ง 2 คน
  ├─ รอบที่ 2: การ์ดลำดับ 2 ของทั้ง 2 คน
  ├─ รอบที่ 3: การ์ดลำดับ 3 ของทั้ง 2 คน
  ├─ รอบที่ 4: การ์ดลำดับ 4 ของทั้ง 2 คน
  └─ รอบที่ 5: การ์ดลำดับ 5 ของทั้ง 2 คน
  ↓
แต่ละรอบ:
  ├─ เปรียบเทียบพลัง (animation 3 วินาที)
  ├─ แสดงผลต่างพลัง
  ├─ กด Enter → แสดงผลรอบนี้
  └─ กด Enter → ไปรอบถัดไป
  ↓
จบเกมเมื่อ:
  ├─ มีคนชนะ 3 รอบก่อน หรือ
  └─ ครบ 5 รอบ (ดูว่าใครชนะมากกว่า)
  ↓
แสดงผลสุดท้าย:
  ├─ ผู้ชนะ: +เงิน, +1 แต้มชนะ (rank)
  └─ ผู้แพ้: -เงิน
  ↓
กด Enter → กลับหน้า Loading
```

**ตัวอย่างการเล่น:**
```
Player 1 เลือกลำดับ: A(1), B(2), C(3), D(4), E(5)
Player 2 เลือกลำดับ: F(1), G(2), H(3), I(4), J(5)

รอบ 1: A vs F → A ชนะ (P1: 1, P2: 0)
รอบ 2: B vs G → G ชนะ (P1: 1, P2: 1)
รอบ 3: C vs H → C ชนะ (P1: 2, P2: 1)
รอบ 4: D vs I → D ชนะ (P1: 3, P2: 1)
→ Player 1 ชนะ 3 รอบก่อน! จบเกม
```

### ระบบ Leaderboard
- โหลดข้อมูล Player 1 และ Player 2
- คำนวณแต้มชนะจากการต่อสู้
- เรียงตามแต้มชนะ (มากไปน้อย)
- แสดงใน Profile และหน้า Leaderboard แยก

### ระบบ Animation
- **Card Flip**: เปลี่ยนจากการ์ดหลังเป็นหน้า
- **Coin Animation**: ตัวเลขลอยขึ้นและ fade out
- **Fade Transition**: เปลี่ยนหน้าแบบ fade in/out

## 📊 ข้อมูลตัวละคร

### Rarity และ Power
- **Rare**: Power 100-300
- **Epic**: Power 400-600
- **Legendary**: Power 700-900
- **Extreme**: Power 1000+

### Drop Rates
**Mystic Chest:**
- Rare: 79%
- Epic: 19%
- Legendary: 1%

**Celestial Chest:**
- Rare: 70%
- Epic: 25%
- Legendary: 4%
- Extreme: 1%

## 🎨 Assets ที่ต้องมี

### รูปภาพ
- `backgrounds/`: town_1.png, town_2.png, summon_1.png, summon_2.png, book.png, arena.png
- `portraits/`: hero1.png - hero21.png
- `cards/front/`: hero1.png - hero21.png
- `cards/back/`: 1.PNG, 2.PNG, 3.PNG (ตาม rarity)
- `ui/`: ปุ่มต่างๆ, กรอบ, ไอคอน, left botton.png, right botton.png
- `How_to_play/`: 1.png - 17.png

### เสียง
- `song/bgm.mp3`: เพลงพื้นหลัง

### ฟอนต์
- `fonts/Monocraft.ttf`: ฟอนต์หลัก

## 🔧 การปรับแต่ง

### เพิ่มตัวละครใหม่
1. เพิ่มข้อมูลใน `src/data/hero_data.py`
2. เพิ่มรูปใน `assets/portraits/` และ `assets/cards/front/`
3. อัปเดต `TOTAL_HEROES` ใน `src/core/config.py`

### เพิ่มโค้ดใหม่
แก้ไข `data/json/codes.json`:
```json
{
  "NEWCODE": {
    "coins": 500,
    "description": "Special bonus"
  }
}
```

### ปรับ Drop Rate
แก้ไขใน:
- `src/screen/mystic_chest_state.py` → `self.mystic_rates`
- `src/screen/celestial_chest_state.py` → `self.celestial_rates`

## 📝 หมายเหตุ

- เกมรองรับ 2 ผู้เล่น (Player 1 และ Player 2)
- ข้อมูลแต่ละคนแยกกันอย่างสมบูรณ์
- โค้ดแต่ละตัวใช้ได้ครั้งเดียวต่อผู้เล่น
- ระบบบันทึกอัตโนมัติเมื่อมีการเปลี่ยนแปลง

## 🐛 Debug

หากเกิดปัญหา ตรวจสอบ:
1. ไฟล์ assets ครบหรือไม่
2. Python version (แนะนำ 3.8+)
3. Pygame version (แนะนำ 2.0+)
4. Console output สำหรับ error messages

---

Made with ❤️ using Python & Pygame
