import pygame

from .game_object import GameObject
from src.utils import DARK_BLUE, MAIN_FONT_PATH


class GameInfo(GameObject):
    def __init__(
            self,
            screen: pygame.Surface,
            position: tuple[int, int],
            size: int = 40,
            text: str = '00',
            color: tuple = DARK_BLUE,
            is_center_pos: bool = False):
        super().__init__(screen)

        self.screen_rect = self.screen.get_rect()

        self.size = size
        self.text = text
        self.__color = color
        self.__font = pygame.font.Font(MAIN_FONT_PATH, self.size)

        self.position = position
        self.x, self.y = self.position
        self.__is_center_pos = is_center_pos

        self.render()

    def convert_to_image(self):
        lines = self.text.split('\n')

        self.text_imgs = []
        self.text_rects = []

        for i, line in enumerate(lines):
            text_img = self.__font.render(line, True, self.__color)
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
        self.convert_to_image()

        if self.__is_center_pos:
            for text_rect in self.text_rects:
                text_rect.center = self.x, self.y

        for text_img, text_rect in zip(self.text_imgs, self.text_rects):
            self.screen.blit(text_img, text_rect)
