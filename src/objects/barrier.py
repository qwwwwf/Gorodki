import pygame

from ..utils import BLACK
from ..objects import GameObject, Bat


class Barrier(GameObject):
    def __init__(self, screen: pygame.Surface, bat: Bat, speed: int | float = 3.75):
        super().__init__(screen)

        self.__bat = bat
        self.__speed = speed
        self.__delta = 20
        self.__is_right_move = True

        self.x = 350
        self.y = 300
        self.is_visible = False

        self.__width = 100
        self.__height = 5

        # Создание прямоугольника
        self.rect_surface = pygame.Surface((self.__width, self.__height), pygame.SRCALPHA)
        self.rect_surface.fill(BLACK)

        self.rect = self.rect_surface.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.rect_surface)

    def get_rect(self):
        return self.rect

    def get_mask(self):
        return self.mask

    def __check_collision(self) -> bool:
        bat_mask = self.__bat.mask
        bat_rect = self.__bat.rect

        offset_x = bat_rect.x - self.rect.x
        offset_y = bat_rect.y - self.rect.y

        return self.mask.overlap(bat_mask, (offset_x, offset_y)) is not None

    def draw(self):
        self.screen.blit(self.rect_surface, self.rect.topleft)

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

        self.rect.topleft = (self.x, self.y)
        self.mask = pygame.mask.from_surface(self.rect_surface)

        # Проверка столкновения с битой
        if self.__bat is not None and self.__check_collision():
            self.__bat.return_to_launch_line()

        self.draw()

    def render(self):
        if self.is_visible:
            self.update()
