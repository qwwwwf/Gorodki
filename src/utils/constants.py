import pygame
from src.utils.loaders import load_image

# Colors
BLUE = (116, 208, 221)
DARK_BLUE = (6, 58, 69)
LIGHT_BLUE = (173, 225, 236)

# Game's settings
SIZE = WIDTH, HEIGHT = 700, 800
GAME_FPS = 60

DEFAULT_BIT_SPEED = 8  # pixels per second
DEFAULT_FIGURE_SPEED = 10  # pixels per second

DEFAULT_GAME_TIME = 120  # seconds

# Sprites
tile_images = {
    'part': load_image('part_of_figure.png')
}

all_sprites = pygame.sprite.Group()
empty_group = pygame.sprite.Group()
parts_group = pygame.sprite.Group()
