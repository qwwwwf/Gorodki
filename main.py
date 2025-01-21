import pygame_menu

from src.utils import *
from src.objects import *
from src.database.db import DataBase
from src.components.game_screen import Game


class MainWindow:
    def __init__(self):
        self.db = DataBase()

        pygame.init()
        pygame.display.set_caption('Городки')

        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()

        self.is_classic_game = True

        self.__theme = pygame_menu.themes.THEME_DARK.copy()
        self.__theme.widget_font = 'src/resources/fonts/PIXY.ttf'
        self.__theme.title_font = 'src/resources/fonts/PIXY.ttf'
        self.__theme.title_font_size = 45
        self.__theme.widget_font_size = 45
        self.__theme.background_color = pygame_menu.baseimage.BaseImage('src/resources/images/background.png')

        self.start()

    def terminate(self):
        pygame.quit()
        self.db.close()
        sys.exit()

    def start(self):
        while True:
            self.start_screen()

    def __change_game_mod(self, value: bool):
        self.is_classic_game = not value

    @staticmethod
    def __change_game_volume(volume: int):
        GAME_VOLUME = volume

    def options_screen(self):
        menu = pygame_menu.Menu('Настройки', 700, 800, theme=self.__theme)

        menu.add.button('Вернуться обратно', self.start_screen)

        menu.add.toggle_switch(
            title='Модификаторы',
            default=0,
            onchange=lambda x: self.__change_game_mod(x)
        )

        menu.add.range_slider(
            title='Громкость звука',
            default=100,
            range_values=list(range(0, 101)),
            range_text_value_enabled=False,
            range_text_value_tick_enabled=False,
            onchange=lambda x: self.__change_game_volume(x)
        )

        menu.mainloop(surface=self.screen)

    def stats_screen(self):
        menu = pygame_menu.Menu('Меню', 700, 800, theme=self.__theme)
        menu.add.button('Вернуться обратно', self.start_screen)

        menu.mainloop(surface=self.screen)

    def start_screen(self):
        menu = pygame_menu.Menu('Меню', 700, 800, theme=self.__theme)

        menu.add.button('Играть', lambda: Game(self))
        menu.add.button('Статистика', lambda: self.stats_screen())
        menu.add.button('Настройки', lambda: self.options_screen())
        menu.add.button('Выйти из игры', pygame_menu.events.EXIT)

        menu.mainloop(surface=self.screen)


if __name__ == '__main__':
    MainWindow()
