import pygame
import random

from ..utils import DARK_BLUE, DEFAULT_GAME_GRAVITY, all_sprites, tile_images, WIDTH, HEIGHT


# Эффект партиклов
class Particle(pygame.sprite.Sprite):
    fire = [tile_images['part_of_field']]

    for scale in (10, 15, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, position: tuple, dx: int, dy: int):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = position

        self.gravity = DEFAULT_GAME_GRAVITY

    def update(self, screen_rect: tuple = (0, 0, WIDTH, HEIGHT)):
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
