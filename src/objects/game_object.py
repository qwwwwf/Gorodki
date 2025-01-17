import pygame


class GameObject:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screen_size = self.screen_width, self.screen_height = self.screen.get_size()

    def render(self):
        pass
