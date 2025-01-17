import pygame
from pygame.draw_py import draw_line

from .game_object import GameObject
from ..utils import DEFAULT_BIT_SPEED, DARK_BLUE


class Bat(GameObject):
    def __init__(
            self,
            screen: pygame.Surface,
            speed: int | float = DEFAULT_BIT_SPEED,
            angle_of_movement: int = 90,
            is_explosive: bool = False
    ):
        super().__init__(screen)

        self.x = 285
        self.is_right_move = True

        self.speed = speed
        self.auto_delay = 5
        self.is_explosive = is_explosive
        self.angle_of_movement = angle_of_movement

        self.__is_thrown = False
        self.is_moving = False

    def thrown(self):
        self.__is_thrown = True

    def draw(self):
        pygame.draw.rect(self.screen, DARK_BLUE, (self.x, 715, 130, 5))

    def update(self):
        if self.is_moving and not self.__is_thrown:
            if self.is_right_move:
                self.x += self.speed
            else:
                self.x -= self.speed

        self.draw()

    def render(self):
        self.update()
