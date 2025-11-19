"""โมเดลข้อมูลฮีโร่และฐานข้อมูล"""
from typing import Optional
from math import sqrt, pow
import pygame


class Character:
    
    def __init__(self, id: int, name: str, rarity: str, atk: int, defense: int, 
                 portrait_path: str, card_front_path: str, card_back_path: str):
        self.id = id
        self.name = name
        self.rarity = rarity
        self.atk = atk
        self.defense = defense
        self.totalPower = round(sqrt(pow(self.atk, 2) + pow(self.defense, 2)))
        self.portrait_path = portrait_path
        self.card_front_path = card_front_path
        self.card_back_path = card_back_path
        self._portrait_surface: Optional[pygame.Surface] = None
        self._card_front_surface: Optional[pygame.Surface] = None
        self._card_back_surface: Optional[pygame.Surface] = None
    
    @property
    def power(self):
        return self.totalPower
    
    @property
    def stats(self):
        return {
            'ATK': self.atk,
            'DEF': self.defense
        }
    
    def get_portrait(self, asset_manager=None) -> pygame.Surface:
        if self._portrait_surface is None:
            if asset_manager:
                self._portrait_surface = asset_manager.load_image(self.portrait_path)
            else:
                self._portrait_surface = pygame.image.load(self.portrait_path).convert_alpha()
        return self._portrait_surface
    
    def get_card_front(self, asset_manager=None) -> pygame.Surface:
        if self._card_front_surface is None:
            if asset_manager:
                self._card_front_surface = asset_manager.load_image(self.card_front_path)
            else:
                self._card_front_surface = pygame.image.load(self.card_front_path).convert_alpha()
        return self._card_front_surface
    
    def get_card_back(self, asset_manager=None) -> pygame.Surface:
        if self._card_back_surface is None:
            if asset_manager:
                self._card_back_surface = asset_manager.load_image(self.card_back_path)
            else:
                self._card_back_surface = pygame.image.load(self.card_back_path).convert_alpha()
        return self._card_back_surface
    
    def __repr__(self):
        return f"Character(id={self.id}, name='{self.name}', rarity='{self.rarity}', power={self.totalPower})"

CHARACTER: list[Character] = [
    Character(
        id=1,
        name='Earth Knight',
        rarity='rare',
        atk=600,
        defense=660,
        portrait_path='assets/portraits/hero1.png',
        card_front_path='assets/cards/front/hero1.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=2,
        name='Crystal Girl',
        rarity='rare',
        atk=850,
        defense=500,
        portrait_path='assets/portraits/hero2.png',
        card_front_path='assets/cards/front/hero2.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=3,
        name='Abyss Hunter',
        rarity='rare',
        atk=820,
        defense=760,
        portrait_path='assets/portraits/hero3.png',
        card_front_path='assets/cards/front/hero3.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=4,
        name='Light Knight',
        rarity='rare',
        atk=650,
        defense=850,
        portrait_path='assets/portraits/hero4.png',
        card_front_path='assets/cards/front/hero4.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=5,
        name='Nocturne',
        rarity='rare',
        atk=750,
        defense=600,
        portrait_path='assets/portraits/hero5.png',
        card_front_path='assets/cards/front/hero5.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=6,
        name='Gale',
        rarity='rare',
        atk=680,
        defense=750,
        portrait_path='assets/portraits/hero6.png',
        card_front_path='assets/cards/front/hero6.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=7,
        name='Inferno',
        rarity='rare',
        atk=780,
        defense=650,
        portrait_path='assets/portraits/hero7.png',
        card_front_path='assets/cards/front/hero7.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=8,
        name='Wind Warlock',
        rarity='rare',
        atk=860,
        defense=750,
        portrait_path='assets/portraits/hero8.png',
        card_front_path='assets/cards/front/hero8.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=9,
        name='Aqua Maiden',
        rarity='rare',
        atk=870,
        defense=620,
        portrait_path='assets/portraits/hero9.png',
        card_front_path='assets/cards/front/hero9.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=10,
        name='Water Sorcerer',
        rarity='rare',
        atk=780,
        defense=670,
        portrait_path='assets/portraits/hero10.png',
        card_front_path='assets/cards/front/hero10.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=11,
        name='Handsome Boy',
        rarity='epic',
        atk=1,
        defense=1800,
        portrait_path='assets/portraits/hero11.png',
        card_front_path='assets/cards/front/hero11.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=12,
        name='Evalyn',
        rarity='epic',
        atk=900,
        defense=750,
        portrait_path='assets/portraits/hero12.png',
        card_front_path='assets/cards/front/hero12.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=13,
        name='Ice Mage',
        rarity='epic',
        atk=1100,
        defense=600,
        portrait_path='assets/portraits/hero13.png',
        card_front_path='assets/cards/front/hero13.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=14,
        name='Malanaya',
        rarity='epic',
        atk=700,
        defense=600,
        portrait_path='assets/portraits/hero14.png',
        card_front_path='assets/cards/front/hero14.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=15,
        name='Chartma',
        rarity='epic',
        atk=700,
        defense=600,
        portrait_path='assets/portraits/hero15.png',
        card_front_path='assets/cards/front/hero15.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=16,
        name='Mercus',
        rarity='epic',
        atk=800,
        defense=1000,
        portrait_path='assets/portraits/hero16.png',
        card_front_path='assets/cards/front/hero16.png',
        card_back_path='assets/cards/back/1.PNG',
    ),
    Character(
        id=17,
        name='Lunaria',
        rarity='legendary',
        atk=1800,
        defense=1200,
        portrait_path='assets/portraits/hero17.png',
        card_front_path='assets/cards/front/hero17.png',
        card_back_path='assets/cards/back/2.PNG',
    ),
    Character(
        id=18,
        name='Light Priestess',
        rarity='legendary',
        atk=1800,
        defense=1000,
        portrait_path='assets/portraits/hero18.png',
        card_front_path='assets/cards/front/hero18.png',
        card_back_path='assets/cards/back/2.PNG',
    ),
    Character(
        id=19,
        name='Karimson Chasha',
        rarity='legendary',
        atk=2000,
        defense=1000,
        portrait_path='assets/portraits/hero19.png',
        card_front_path='assets/cards/front/hero19.png',
        card_back_path='assets/cards/back/2.PNG',
    ),
    Character(
        id=20,
        name='Golden Dragon',
        rarity='extreme',
        atk=2500,
        defense=2300,
        portrait_path='assets/portraits/hero20.png',
        card_front_path='assets/cards/front/hero20.png',
        card_back_path='assets/cards/back/3.PNG',
    ),
    Character(
        id=21,
        name='Nailung',
        rarity='extreme',
        atk=2300,
        defense=2000,
        portrait_path='assets/portraits/hero21.png',
        card_front_path='assets/cards/front/hero21.png',
        card_back_path='assets/cards/back/3.PNG',
    ),
]


# สร้าง dictionary สำหรับการเข้าถึงแบบเร็ว
HERO_DATABASE = {char.id: char for char in CHARACTER}


def get_hero(hero_id: int) -> Optional[Character]:
    return HERO_DATABASE.get(hero_id)


def get_heroes_by_rarity(rarity: str) -> list[Character]:
    return [char for char in CHARACTER if char.rarity == rarity.lower()]


def get_all_heroes() -> list[Character]:
    return CHARACTER.copy()


def get_total_heroes() -> int:
    return len(CHARACTER)
Hero = Character
