from pygame.math import Vector2
from pathlib import Path

#BASEDIR
CHARACTER_DIR = Path(__file__).resolve().parent.parent/'graphics'/'character'
OVERLAY_DIR = Path(__file__).resolve().parent.parent/'graphics'/'overlay'
WORLD_DIR = Path(__file__).resolve().parent.parent/'graphics'/'world'
DATA_DIR = Path(__file__).resolve().parent.parent/'data'
WATER_DIR = Path(__file__).resolve().parent.parent/'graphics'/'water'
FRUIT_DIR = Path(__file__).resolve().parent.parent/'graphics'/'fruit'
STUMPS_DIR = Path(__file__).resolve().parent.parent/'graphics'/'stumps'
SOIL_DIR = Path(__file__).resolve().parent.parent/'graphics'/'soil'
SOIL_WATER_DIR = Path(__file__).resolve().parent.parent/'graphics'/'soil_water'
RAIN_D_DIR = Path(__file__).resolve().parent.parent/'graphics'/'rain'/'drops'
RAIN_F_DIR = Path(__file__).resolve().parent.parent/'graphics'/'rain'/'floor'
FONT_DIR = Path(__file__).resolve().parent.parent/'font'
AUDIO_DIR = Path(__file__).resolve().parent.parent/'audio'


#GAME SCREEN
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

#OVERLAY POSITIONS
OVERLAY_POSITIONS = {
    'tool': (40, SCREEN_HEIGHT - 15),
    'seed': (70, SCREEN_HEIGHT - 5),
}

PLAYER_TOOL_OFFSET = {
    'left': Vector2(-50, 40),
    'right': Vector2(50, 40),
    'up': Vector2(0, -10),
    'down': Vector2(0, 50),
}

LAYERS = {
    'water': 0,
    'ground': 1, 
    'soil': 2,
    'soil water': 3, 
    'rain floor': 4, 
    'house bottom': 5, 
    'ground plant': 6,
    'main': 7,
    'house top': 8,
    'fruit': 9,
    'rain drops': 10,
}

APPLE_POS = {
    'Small': [(18,17), (30, 37), (12, 50), (30, 45), (20, 30), (30, 10)],
    'Large': [(30, 24), (60, 65), (50, 50), (16, 40), (45, 50), (42, 70)],
}

GROW_SPEED = {
    'corn': 1,
    'tomato': 0.7,
}

SALE_PRICES = {
    'wood': 4,
    'apple': 2,
    'corn': 10,
    'tomato': 20,
}

PURCHASE_PRICES = {
    'corn': 4,
    'tomato': 5,
}
 
