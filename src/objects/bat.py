import math
import pygame

from cachetools import TTLCache
from ..objects.game_object import GameObject
from ..objects.launch_line import LaunchLine
from ..utils import DEFAULT_BIT_SPEED, DARK_BLUE, parts_group


class Bat(GameObject, pygame.sprite.Sprite):
    def __init__(
            self,
            screen: pygame.Surface,
            game_object,
            launch_line: LaunchLine,
            speed: int | float = DEFAULT_BIT_SPEED,
            angle_of_movement: int = 90,
            is_explosive: bool = False
    ):
        super().__init__(screen)
        pygame.sprite.Sprite.__init__(self)

        self.game_object = game_object
        self.launch_line = launch_line

        self.x = 340
        self.y = 685

        self.speed = speed
        self.speed_boost = 1
        self.is_moving = False
        self.is_thrown = False
        self.is_right_move = True

        self.auto_delay = 5
        self.thrown_count = 0
        self.figures_knocked = 0

        self.is_explosive = is_explosive
        self.extension_factor = 1
        self.angle_of_movement = angle_of_movement if 60 <= angle_of_movement <= 120 else 90

        self.__angle = 0
        self.__rps = 6

        self.__throw_sound = pygame.mixer.Sound('src/resources/sounds/throw_sound.wav')
        self.__throw_sound.set_volume(0.2)
        self.__is_sound_playing = False
        self.__max_collision_sounds = 4
        self.__collision_sounds_cache = TTLCache(self.__max_collision_sounds, 0.5)

        # Создание прямоугольника
        self.rect_width = 90
        self.rect_height = 5
        self.rect_surface = pygame.Surface((self.rect_width * self.extension_factor, self.rect_height), pygame.SRCALPHA)
        self.rect_surface.fill(DARK_BLUE)

        self.rect = self.rect_surface.get_rect(topleft=(self.x, self.y))
        self.mask = pygame.mask.from_surface(self.rect_surface)

    def return_to_launch_line(self):
        # Проверка попал ли игрок в фигуру
        if self.launch_line.is_changeable:
            if self.game_object.last_parts_count == len(parts_group):
                self.launch_line.y = 180
            else:
                self.launch_line.y = 120
                self.game_object.last_parts_count = len(parts_group)

        self.x = 340
        self.y = self.launch_line.y
        self.is_thrown = False
        self.__stop_throw_sound()

    def __play_throw_sound(self):
        if not self.__is_sound_playing:
            self.__throw_sound.play(-1)
            self.__is_sound_playing = True

    def __stop_throw_sound(self):
        if self.__is_sound_playing:
            self.__throw_sound.stop()
            self.__is_sound_playing = False

    def __play_collision_sound(self, part):
        if len(self.__collision_sounds_cache) < self.__max_collision_sounds:
            self.__collision_sounds_cache[part.rect.x] = None
            part.collision_sound.play()

    def throw(self):
        if not self.is_thrown:
            self.__play_throw_sound()
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

        self.__angle += self.__rps * self.speed_boost * 0.9
        if self.__angle >= 360:
            self.__angle = 0

        if self.is_thrown:
            radians = math.radians(self.angle_of_movement)
            self.x += self.speed * math.cos(radians)
            self.y -= self.speed * self.speed_boost * 0.95 * math.sin(radians)

            if self.y < -20 or 0 >= self.x >= self.screen_width:
                self.return_to_launch_line()

        # Обнаружение столкновения
        rotated_surface = pygame.transform.rotate(self.rect_surface, self.__angle)
        self.rect = rotated_surface.get_rect(center=(self.x, self.y))
        self.mask = pygame.mask.from_surface(rotated_surface)

        for part in parts_group:
            if not part.is_knocked:
                if pygame.sprite.collide_mask(self, part):
                    if self.is_explosive:
                        for i, part in enumerate(parts_group, 1):
                            part.speed_y = -2.65 * i
                            part.is_knocked = True
                            self.__play_collision_sound(part)
                            self.game_object.parts_knocked += len(parts_group)
                        break

                    part.speed_y = -10
                    part.is_knocked = True
                    self.game_object.parts_knocked += 1
                    self.__play_collision_sound(part)

        # Отрисовка биты
        self.draw()

    def render(self):
        self.update()
