import pygame
from ..utils import load_image


# Colors
BLACK = (0, 0, 0)
BLUE = (116, 208, 221)
DARK_BLUE = (6, 58, 69)
LIGHT_BLUE = (173, 225, 236)

# Game's settings
SIZE = WIDTH, HEIGHT = 700, 800

GAME_FPS = 60
GAME_VOLUME = 1  # 0.00 - 1.00 (0% - 100%)

DEFAULT_BIT_SPEED = 6.5  # pixels per second
DEFAULT_FIGURE_SPEED = 3.1 # pixels per second
DEFAULT_GAME_GRAVITY = 1

DEFAULT_GAME_TIME = 120  # seconds

# Sprites
tile_images = {
    'part': load_image('part_of_figure.png'),
    'part_of_field': load_image('part_of_field.png')
}

all_sprites = pygame.sprite.Group()
parts_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()

# Const info
names_of_modifiers = {
    1: 'ускорение',
    2: 'замедление',
    3: 'взрывная бита',
    4: 'бита летит\nпод углом',
    5: 'измененная длина\nбиты',
    6: 'препятствие',
    7: 'игровое время\nувеличено',
    8: 'игровое время\nукорочено',
    9: 'линия запуска\nне меняется'
}
