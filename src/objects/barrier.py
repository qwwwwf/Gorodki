import pygame

from ..utils import BLACK
from .game_object import GameObject


class Barrier(GameObject):
    def __init__(self, screen: pygame.Surface, speed: int | float = 4.25):
        super().__init__(screen)

        self.__speed = speed
        self.__delta = 20
        self.__is_right_move = True

        self.x = 350
        self.y = 300

        self.__width = 100
        self.__height = 5


    def draw(self):
        pygame.draw.rect(self.screen, BLACK, (self.x, self.y, self.__width, self.__height))

    def update(self):
        if self.__is_right_move:
            future_x = self.x + self.__speed

            if future_x < self.screen_width - 100 - self.__delta:
                self.x += self.__speed
            else:
                self.__is_right_move = False
        else:
            future_x = self.x - self.__speed

            if future_x > self.__delta:
                self.x -= self.__speed
            else:
                self.__is_right_move = True

        self.draw()

    def render(self):
        self.update()
