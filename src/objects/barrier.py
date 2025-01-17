import pygame
from .game_object import GameObject


class Barrier(GameObject):
    def __init__(self, screen: pygame.Surface, speed: int | float = 5):
        super().__init__(screen)

        self.speed = speed
