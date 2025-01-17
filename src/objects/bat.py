import pygame
from .game_object import GameObject


class Bat(GameObject):
    def __init__(
            self,
            screen: pygame.Surface,
            speed: int | float = 10,
            angle_of_movement: int = 90,
            is_explosive: bool = False
    ):
        super().__init__(screen)

        self.__rps = 5
        self.speed = speed
        self.is_explosive = is_explosive
        self.angle_of_movement = angle_of_movement
        self.is_moving = False
