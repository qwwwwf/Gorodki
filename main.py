import pygame_menu

from src.utils import *
from src.objects import *
from src.components.game_screen import Game
from src.database.db import DataBase, Passing, Settings


class MainWindow:
    def __init__(self):
        self.db = DataBase()
        self.db_passing = Passing()
        self.db_player_settings = Settings()

        self.db.create_tables()
        self.db_player_settings.create()

        pygame.init()
        pygame.display.set_caption('Городки')
        pygame.display.set_icon(pygame.image.load('src/resources/images/logo.ico'))

        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()

        self.__player_settings = self.db_player_settings.get()
        self.__stats_sort_id = 0
        self.game_volume = self.__player_settings[1]
        self.is_classic_game = self.__player_settings[2]

        self.__theme = pygame_menu.themes.THEME_DARK.copy()
        self.__theme.widget_font = MAIN_FONT_PATH
        self.__theme.title_font = MAIN_FONT_PATH
        self.__theme.title_font_size = 45
        self.__theme.widget_font_size = 45
        self.__theme.background_color = pygame_menu.baseimage.BaseImage('src/resources/images/background.png')
        self.__theme.selection_color = LIGHT_BLUE

        self.start_screen()

    def terminate(self):
        pygame.quit()
        self.db.close()
        sys.exit()

    def __change_game_mod(self, value: bool):
        self.is_classic_game = not value
        self.db_player_settings.update_values({'gameWithModifiers': self.is_classic_game})

    def __change_game_volume(self, volume: int):
        self.game_volume = volume / 100
        self.db_player_settings.update_values({'gameVolume': self.game_volume})

    def __change_stats_sort(self, sort_id: int):
        self.__stats_sort_id = sort_id
        self.stats_screen()

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
        menu.add.button('Вернуться назад', self.start_screen)

        menu.add.toggle_switch(
            title='Модификаторы',
            default=not self.is_classic_game,
            onchange=lambda x: self.__change_game_mod(x)
        )

        menu.add.range_slider(
            title='Громкость звука',
            default=self.game_volume * 100,
            range_values=list(range(0, 101)),
            range_text_value_enabled=False,
            range_text_value_tick_enabled=False,
            onchange=lambda x: self.__change_game_volume(x)
        )

        menu.mainloop(surface=self.screen)

    def stats_screen(self):
        menu = pygame_menu.Menu('Статистика', 700, 800, theme=self.__theme)
        menu.add.button(
            title='Вернуться назад',
            action=self.start_screen,
            padding=5
        )

        menu.add.dropselect(
            title='Сортировка',
            items=[('По порядку', 0), ('Очки', 1), ('Брошено бит', 2), ('Сбито фигур', 3), ('Долгие игры', 4)],
            default=self.__stats_sort_id,
            onchange=lambda a, b: self.__change_stats_sort(b),
            font_size=25,
            placeholder='Выберите сортировку',
            selection_box_bgcolor=LIGHT_BLUE
        )

        games_stat_texts = list(map(
            lambda x: f'Игра #{x[0]}\nСчёт: {x[1]}\nФигур сбито: {x[2]}\nБрошено бит: {x[3]}\nБонус: '
                      f'{str(x[4]).replace("0", "не пройден").replace("1", "пройден")}\nПройдено за {x[5]} сек.',
            self.db_passing.get_all(sort_id=self.__stats_sort_id))
        )

        if games_stat_texts:
            best_result = self.db_passing.get_best_result()

            menu.add.label(
                title=f'\nЛучший результат: {best_result[1]}\n(игра #{best_result[0]})\n\n' + f'\n{"-" * 30}\n'.join(games_stat_texts),
                font_size=30
            )
        else:
            menu.add.label('История игр пуста')

        menu.mainloop(surface=self.screen)

    def start_screen(self):
        menu = pygame_menu.Menu('Меню', 700, 800, theme=self.__theme)

        menu.add.image(image_path='src/resources/images/logo.png', scale=(0.2, 0.2), margin=(0, 75))

        menu.add.button('Играть', lambda: Game(self))
        menu.add.button('Статистика', lambda: self.stats_screen())
        menu.add.button('Настройки', lambda: self.options_screen())
        menu.add.button('Выйти из игры', pygame_menu.events.EXIT)

        menu.mainloop(surface=self.screen)


if __name__ == '__main__':
    MainWindow()
