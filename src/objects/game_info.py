import pygame

from src.utils import DARK_BLUE
from .game_object import GameObject


class GameInfo(GameObject):
    def __init__(self, screen: pygame.Surface, x: int, y: int, size: int = 40, text: str = '00'):
        super().__init__(screen)

        self.screen_rect = self.screen.get_rect()

        self.size = size
        self.text =text
        self.color = DARK_BLUE
        self.font = pygame.font.Font('src/fonts/PIXY.ttf', self.size)

        self.x = x
        self.y = y

        self.render()

    def convert_to_image(self, text: str):
        lines = text.split('\n')

        self.text_imgs = []
        self.text_rects = []

        for i, line in enumerate(lines):
            text_img = self.font.render(line, True, self.color)
            text_rect = text_img.get_rect()

            if self.x >= 0:
                text_rect.left = self.x
            else:
                text_rect.right = self.screen_rect.width + self.x

            if self.y >= 0:
                text_rect.top = self.y + i * self.size
            else:
                text_rect.bottom = self.screen_rect.height + self.y + i * self.size

            self.text_imgs.append(text_img)
            self.text_rects.append(text_rect)

    def render(self):
        self.convert_to_image(self.text)
        for text_img, text_rect in zip(self.text_imgs, self.text_rects):
            self.screen.blit(text_img, text_rect)
