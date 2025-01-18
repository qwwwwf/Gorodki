import math
import pygame

from .game_object import GameObject
from ..utils import DEFAULT_BIT_SPEED, DARK_BLUE, parts_group


class Bat(GameObject, pygame.sprite.Sprite):
    def __init__(
            self,
            screen: pygame.Surface,
            speed: int | float = DEFAULT_BIT_SPEED,
            angle_of_movement: int = 90,
            is_explosive: bool = False
    ):
        super().__init__(screen)
        pygame.sprite.Sprite.__init__(self)

        self.x = 340
        self.y = 685
        self.launch_line_y = self.y

        self.is_moving = False
        self.is_thrown = False
        self.is_right_move = True

        self.speed = speed
        self.auto_delay = 5
        self.thrown_count = 0
        self.figures_knocked = 0
        self.is_explosive = is_explosive
        self.angle_of_movement = angle_of_movement if 45 <= angle_of_movement <= 120 else 90

        self.__angle = 0
        self.__rps = 6
        self.__speed_boost = 1

        # Поверхность для прямоугольника
        self.rect_width = 90
        self.rect_height = 5
        self.rect_surface = pygame.Surface((self.rect_width, self.rect_height), pygame.SRCALPHA)
        self.rect_surface.fill(DARK_BLUE)

        # Маска прямоугольника
        self.rect = self.rect_surface.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.rect_surface)

    def throw(self):
        if not self.is_thrown:
            self.is_thrown = True
            self.auto_delay = 5
            self.thrown_count += 1

    def draw(self):
        rotated_surface = pygame.transform.rotate(self.rect_surface, self.__angle)
        rotated_rect = rotated_surface.get_rect(center=(self.x, self.y))

        self.screen.blit(rotated_surface, rotated_rect.topleft)

    def update(self):
        if self.is_moving and not self.is_thrown:
            if self.is_right_move:
                if self.x + self.speed <= self.screen_width - 50:
                    self.x += self.speed
            else:
                if self.x - self.speed >= 50:
                    self.x -= self.speed

        self.__angle += self.__rps * self.__speed_boost * 0.9
        if self.__angle >= 360:
            self.__angle = 0

        if self.is_thrown:
            radians = math.radians(self.angle_of_movement)
            self.x += self.speed * math.cos(radians)
            self.y -= self.speed * self.__speed_boost * 0.95 * math.sin(radians)

            if self.y < -20 or 0 >= self.x >= self.screen_width:
                self.x = 340
                self.y = 685
                self.is_thrown = False

        # Обнаружение столкновения
        rotated_surface = pygame.transform.rotate(self.rect_surface, self.__angle)
        self.rect = rotated_surface.get_rect(center=(self.x, self.y))  # Обновляем rect с учетом вращения
        self.mask = pygame.mask.from_surface(rotated_surface)

        for part in parts_group:
            if pygame.sprite.collide_mask(self, part):
                if self.is_explosive:
                    for part in parts_group:
                        part.speed_y = -10
                        part.is_knocked = True
                    break

                part.speed_y = -10
                part.is_knocked = True


        # Отрисовка биты
        self.draw()

    def render(self):
        self.update()
