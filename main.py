import pygame_menu

from src.utils import *
from src.objects import *
from src.components.game_screen import Game
from src.database.db import DataBase, Passing, Player


class MainWindow:
    def __init__(self):
        self.db = DataBase()
        self.db_passing = Passing()
        self.db_player = Player()

        self.db.create_tables()
        self.db_player.create()

        pygame.init()
        pygame.display.set_caption('Городки')

        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()

        self.is_classic_game = True

        self.__theme = pygame_menu.themes.THEME_DARK.copy()
        self.__theme.widget_font = MAIN_FONT_PATH
        self.__theme.title_font = MAIN_FONT_PATH
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

    def __change_game_volume(self, volume: int):
        global GAME_VOLUME

        GAME_VOLUME = volume / 100

    def game_stat_screen(self, game_stat: dict):
        if not game_stat:
            self.start_screen()
            return

        menu = pygame_menu.Menu('Игровая статистика', 700, 800, theme=self.__theme)

        menu.add.label(f"""
Счет: {game_stat['score']}
Фигур сбито: {game_stat['figures_knocked']}
Брошено бит: {game_stat['total_bits_thrown']}
Бонус: {'пройден' if game_stat['bonus_level_passed'] else 'не пройден'}
Пройдено за {game_stat['seconds_time_spent']} сек.
        """)
        menu.add.button('В главное меню', self.start_screen)

        menu.mainloop(surface=self.screen)

    def options_screen(self):
        menu = pygame_menu.Menu('Настройки', 700, 800, theme=self.__theme)
        menu.add.button('Вернуться обратно', self.start_screen)

        menu.add.toggle_switch(
            title='Модификаторы',
            default=not self.is_classic_game,
            onchange=lambda x: self.__change_game_mod(x)
        )

        menu.add.range_slider(
            title='Громкость звука',
            default=GAME_VOLUME * 100,
            range_values=list(range(0, 101)),
            range_text_value_enabled=False,
            range_text_value_tick_enabled=False,
            onchange=lambda x: self.__change_game_volume(x)
        )

        menu.mainloop(surface=self.screen)

    def stats_screen(self):
        menu = pygame_menu.Menu('Статистика', 700, 800, theme=self.__theme)
        menu.add.button(
            title='Вернуться обратно',
            action=self.start_screen,
            padding=5
        )

        games_stat_texts = list(map(lambda x: f'{x[1]}/{x[2]}/{x[3]}/{x[4]}/{x[5]} сек.', self.db_passing.get_all()))

        for game_stat in games_stat_texts:
            menu.add.label(
                title=game_stat,
                padding=5,
                font_size=35
            )

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
