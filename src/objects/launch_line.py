import pygame

from src.utils import LIGHT_BLUE
from .game_object import GameObject


class LaunchLine(GameObject):
    def __init__(self, screen: pygame.Surface, y: int = 120):
        super().__init__(screen)

        self.size = self.width, self.height = self.screen_width, 15
        self.x = 0
        self._y = self.screen_height - y
        self.is_changeable = True

    def draw(self):
        pygame.draw.rect(self.screen, LIGHT_BLUE, (self.x, self.y, *self.size))

    def render(self):
        self.draw()

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value: int):
        self._y = self.screen_height - value
