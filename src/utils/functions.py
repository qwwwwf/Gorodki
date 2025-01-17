import pygame
from src.utils.constants import tile_images, parts_group


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(parts_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(25 * pos_x + 255, 25 * pos_y + 75)


def generate_figure(figure_map: list):
    x, y = 0, 0

    for y in range(len(figure_map)):
        for x in range(len(figure_map[y])):
            if figure_map[y][x] == '#':
                Tile('part', x, y)

    return x, y
