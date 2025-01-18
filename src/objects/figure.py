import random
import pygame

from .game_object import GameObject
from src.utils import load_image, load_figure, LIGHT_BLUE, DARK_BLUE, parts_group, tile_images, DEFAULT_FIGURE_SPEED


# Генерация фигуры по её карте
def generate_figure(figure_map: list):
    x, y = 0, 0

    for y in range(len(figure_map)):
        for x in range(len(figure_map[y])):
            if figure_map[y][x] == '#':
                Part(x, y)

    return x, y


class Part(pygame.sprite.Sprite):
    def __init__(self, x: int | float, y: int | float):
        super().__init__(parts_group)
        self.image = tile_images['part']
        self.rect = self.image.get_rect().move(25 * x + 255, 25 * y + 75)
        self.offset_x = x
        self.offset_y = y
        self.speed_y = 0
        self.is_knocked = False

    def update(self):
        if self.is_knocked:
            self.rect.y += self.speed_y

            if self.rect.y < -self.rect.height:
                self.kill()


class Figure(GameObject):
    def __init__(self, screen: pygame.Surface, figure_filename: str, speed: int | float = DEFAULT_FIGURE_SPEED):
        super().__init__(screen)
        self.x = 255
        self.y = 50
        self.field_size = self.field_width, self.field_height = 175, 175
        self.speed = speed

        # Загрузка изображения фигуры
        self.figure_image = load_image('part_of_figure.png')
        self.figure_rect = self.figure_image.get_rect()
        self.figure_map = load_figure(figure_filename)
        generate_figure(self.figure_map)

        self.__delta = 20
        self.__is_moving = True
        self.__is_right_move = False
        self.__speed_boost = 1

    def draw_field(self):
        pygame.draw.rect(self.screen, LIGHT_BLUE, (self.x, self.y, *self.field_size))
        pygame.draw.rect(self.screen, DARK_BLUE, (self.x, self.y, *self.field_size), 3)

    def draw_figure(self):
        for part in parts_group:
            if not part.is_knocked:
                part.rect.x = self.x + part.rect.width * part.offset_x
                part.rect.y = self.y + part.rect.width * part.offset_y
        parts_group.update()

    def update(self):
        if self.__is_moving:
            if self.__is_right_move:
                future_x = self.x + (self.speed * self.__speed_boost)

                if self.x + self.speed < (self.screen_width - self.field_width) - self.__delta // 2:
                    self.x += self.speed * self.__speed_boost
                else:
                    self.__is_right_move = False
                    self.__speed_boost = 1.65

                if future_x >= self.screen_width // 2 - self.__delta:
                    if self.__speed_boost != 1:
                        self.__speed_boost = 1
            else:
                future_x = self.x - (self.speed * self.__speed_boost)

                if future_x > self.__delta:
                    self.x -= self.speed * self.__speed_boost
                else:
                    self.__is_right_move = True
                    self.__speed_boost = 1.55

        self.__delta = random.randint(15, 45)

    def render(self):
        self.update()
        self.draw_field()
        self.draw_figure()
