import pygame
import json
import sys
from pathlib import Path
pygame.init()

base_dir = Path(__file__).resolve().parent
data_part = base_dir / "data.json"
with data_part.open("r") as f:
    data = json.load(f)
    width = data["settings"]["width"]
    height = data["settings"]["height"]
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("TENOI")
clock = pygame.time.Clock()