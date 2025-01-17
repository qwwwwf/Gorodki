import pygame

from .game_object import GameObject
from src.utils import SideEnum, load_image, load_figure, generate_figure, LIGHT_BLUE, DARK_BLUE, parts_group, \
    DEFAULT_FIGURE_SPEED


class Figure(GameObject):
    def __init__(self, screen: pygame.Surface, figure_filename: str, speed: int | float = DEFAULT_FIGURE_SPEED):
        super().__init__(screen)
        self.x = 255
        self.y = 50
        self.field_size = self.field_width, self.field_height = 200, 200
        self.speed = speed

        # Загрузка изображения фигуры
        self.figure_image = load_image('part_of_figure.png')
        self.figure_rect = self.figure_image.get_rect()
        self.figure_map = load_figure(figure_filename)
        generate_figure(self.figure_map)

        self.__delta = 20
        self.__is_moving = True
        self.__side_moving = SideEnum.LEFT
        self.__speed_boost = 1

    def draw_field(self):
        pygame.draw.rect(self.screen, LIGHT_BLUE, (self.x, self.y, *self.field_size))
        pygame.draw.rect(self.screen, DARK_BLUE, (self.x, self.y, *self.field_size), 3)

    def draw_figure(self):
        # TODO: сделать совместное движение с полем фигуры
        move_reverse = 1

        if self.__side_moving == SideEnum.LEFT:
            move_reverse = -1

        for part in parts_group:
            part.rect.x += self.speed * self.__speed_boost * move_reverse

    def update(self):
        if self.__is_moving:
            match self.__side_moving:
                case SideEnum.LEFT:
                    future_x = self.x - (self.speed * self.__speed_boost)

                    if future_x > self.__delta:
                        self.x -= self.speed * self.__speed_boost
                    else:
                        self.__side_moving = SideEnum.RIGHT
                        self.__speed_boost = 1.5

                case SideEnum.RIGHT:
                    future_x = self.x - (self.speed * self.__speed_boost)

                    if self.x + self.speed < (self.screen_width - self.field_width) - self.__delta // 2:
                        self.x += self.speed * self.__speed_boost
                    else:
                        self.__side_moving = SideEnum.LEFT
                        self.__speed_boost = 1.75

                    if future_x >= self.screen_width // 2 - self.__delta:
                        if self.__speed_boost != 1:
                            self.__speed_boost = 1

    def render(self):
        self.update()
        self.draw_figure()
        self.draw_field()
