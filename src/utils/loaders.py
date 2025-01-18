import os
import sys
import pygame


# Загрузка спрайта
def load_image(filename: str) -> pygame.Surface | None:
    fullname = os.path.join('src/resources/sprites/', filename)

    if not os.path.isfile(fullname):
        print(f'Файл с изображением {fullname} не найден')
        sys.exit()

    image = pygame.image.load(fullname)
    return image


# Загрузка карты фигуры
def load_figure(filename: str) -> list:
    filename = 'src/resources/figures/' + filename

    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))
