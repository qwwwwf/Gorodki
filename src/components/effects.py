import pygame
from src.utils.constants import DARK_BLUE


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
