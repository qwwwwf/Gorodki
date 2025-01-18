import pygame
import random

from src.utils import DARK_BLUE, DEFAULT_GAME_GRAVITY, all_sprites, load_image


# Анимация спрайта
class AnimatedSprite(pygame.sprite.Sprite):
    """
    Создает анимацию и применяет ее к спрайту

    :param sheet: Спрайт с анимацией
    :param columns: Количество колонок у спрайта
    :param rows: Количество рядов у спрайта
    :param x: Изначальное местоположение спрайта на оси абсцисс
    :param y: Изначальное местоположение спрайта на оси ординат
    """

    def __init__(self, sheet: pygame.Surface, columns: int, rows: int, x: int, y: int):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet: pygame.Surface, columns: int, rows: int):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)

        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


# Игровой звук
class GameSound:
    def __init__(self):
        pass

    def play_bat_thrown(self):
        pass

    def play_figure_knocked(self):
        pass


# Эффект партиклов
class Particle(pygame.sprite.Sprite):
    fire = [load_image('star.png')]

    for scale in (10, 15, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = DEFAULT_GAME_GRAVITY

    def update(self, screen_rect: tuple = (0, 0, 700, 800)):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]

        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position: tuple):
    particle_count = 25  # количество частиц
    numbers = range(-6, 6)  # возможные скорости

    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


# Применение эффекта ТВ
def apply_tv_scanlines(
        screen: pygame.Surface,
        time: int,
        speed: int | float = 2.75,
        thickness: int = 25,
        spacing: int = 40,
        opacity: int = 5
):
    """
    Применяет эффект горизонтальных полос, движущихся сверху вниз.

    :param screen: Поверхность PyGame (Surface), к которой применяется эффект
    :param time: Время (в миллисекундах) для анимации
    :param speed: Скорость движения полос
    :param thickness: Толщина полос
    :param spacing: Расстояние между полосами
    :param opacity: Прозрачность полос (от 0 до 255)
    """
    width, height = screen.get_size()

    scanline_surface = pygame.Surface((width, height), pygame.SRCALPHA)

    for y in range(-thickness, height, spacing):
        offset = int(time * 0.1 * speed) % spacing
        pygame.draw.rect(scanline_surface, (*DARK_BLUE, opacity), (0, y + offset, width, thickness))

    screen.blit(scanline_surface, (0, 0))
