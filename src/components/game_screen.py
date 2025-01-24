from ..utils import *
from ..objects import *
from ..components import apply_tv_scanlines, create_particles


class Game:
    def __init__(self, main_window):
        self.main_window = main_window
        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        self.effects_time = 0

        # Game edit
        self.__is_running = True
        self.__bat_limits = 28
        self.__paused = False
        self.__can_create_particles = True

        # Game stats
        self.game_stat = {}
        self.parts_knocked = 0
        self.last_parts_count = 0
        self.game_time = DEFAULT_GAME_TIME
        self.__total_seconds_spent = 0
        self.__bonus_level_is_passed = False
        self.__game_level = 1
        self.__game_modifiers = generate_game_modifiers(self.main_window.is_classic_game)
        self.__game_modifiers_ids = ''.join(
            sorted(list(set(map(str, list(map(lambda x: x[0], self.__game_modifiers))))))).replace('0', '')

        self.run()

    def render_pause(self):
        self.__paused = not self.__paused
        self.bat.stop_throw_sound()

        if not self.__paused and self.bat.is_thrown:
            self.bat.play_throw_sound()

        if self.__paused:
            darken_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            darken_surface.fill((0, 0, 0, 155))
            self.screen.blit(darken_surface, (0, 0))

            GameInfo(
                screen=self.screen,
                position=(WIDTH // 2, HEIGHT // 2),
                size=60,
                text='Пауза',
                color=WHITE,
                is_center_pos=True
            )

            GameInfo(
                screen=self.screen,
                position=(WIDTH // 2, HEIGHT // 2 + 225),
                size=30,
                text='Ctrl+M - выйти в меню',
                color=LIGHT_BLUE,
                is_center_pos=True
            )

    def next_level(self):
        game_modifiers = parse_game_modifiers(self.__game_modifiers, self.bat.figures_knocked)
        self.figure = Figure(self.screen, f'figure{self.__game_level}.txt')
        self.last_parts_count = len(parts_group)

        self.bat.speed_boost = game_modifiers['bat_boost']
        self.figure.default_speed_boost = game_modifiers['figure_boost']
        self.bat.is_explosive = game_modifiers['bat_is_explosive']
        self.bat.angle_of_movement = game_modifiers['bat_has_angular_movement']
        self.bat.extension_factor = game_modifiers['bat_extension']
        self.game_time *= game_modifiers['increase_game_time']
        self.barrier.is_visible = game_modifiers['barrier']
        self.launch_line.is_changeable = not game_modifiers['unchangeable_launch_line']

    def __calc_score(self):
        # Базовые параметры
        figures_knocked = self.bat.figures_knocked
        parts_knocked = self.parts_knocked
        thrown_count = self.bat.thrown_count
        time_bonus = max(0, (DEFAULT_GAME_TIME - self.game_time) * 10)  # Бонус за оставшееся время

        # Множители
        level_multiplier = 10  # Множитель за уровень
        parts_multiplier = 2  # Множитель за сбитые части
        penalty_factor = 5  # Штраф за каждый бросок
        difficulty_factor = 1 + (self.__game_level - 1) * 0.1  # Увеличиваем сложность с каждым уровнем

        # Формула
        score = (
                    (figures_knocked * level_multiplier) +
                    (parts_knocked * parts_multiplier) -
                    (thrown_count * penalty_factor) +
                    time_bonus
                ) * difficulty_factor

        return round(score)

    def stop(self, write_stats: bool = True):
        self.bat.stop_throw_sound()
        self.__is_running = False

        if write_stats:
            self.game_stat = {
                'score': self.__calc_score(),
                'figures_knocked': self.bat.figures_knocked,
                'total_bits_thrown': self.bat.thrown_count,
                'bonus_level_passed': self.__bonus_level_is_passed,
                'seconds_time_spent': round(self.__total_seconds_spent),
                'game_modifiers_ids': self.__game_modifiers_ids
            }

            self.main_window.db_passing.add(**self.game_stat)

    def run(self):
        # Initial game objects
        self.launch_line = LaunchLine(self.screen)
        self.bat = Bat(self.screen, self, self.launch_line)
        self.barrier = Barrier(self.screen, self.bat)
        self.next_level()

        while self.__is_running:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.main_window.terminate()

                    # Если клавиша зажата
                    case pygame.KEYDOWN:
                        ctrl_pressed = pygame.key.get_mods() & pygame.KMOD_CTRL

                        if ctrl_pressed:
                            match event.key:
                                case pygame.K_q:
                                    self.main_window.terminate()

                                case pygame.K_p:
                                    self.render_pause()

                                case pygame.K_m:
                                    self.stop(False)
                        else:
                            match event.key:
                                case pygame.K_LEFT:
                                    self.bat.is_moving = True
                                    self.bat.is_right_move = False

                                case pygame.K_RIGHT:
                                    self.bat.is_moving = True
                                    self.bat.is_right_move = True

                                case pygame.K_SPACE | pygame.K_UP:
                                    self.bat.throw()

                    # Если клавиша отжата
                    case pygame.KEYUP:
                        self.bat.is_moving = False

            if not self.__paused:
                self.screen.fill(BLUE)
                self.game_time -= 1 / GAME_FPS
                self.__total_seconds_spent += 1 / GAME_FPS

                if (not self.bat.is_thrown and self.bat.thrown_count >= self.__bat_limits) or int(self.game_time <= 0):
                    self.stop()

                if not self.bat.is_thrown:
                    self.bat.auto_delay -= 1 / GAME_FPS

                # Render game objects
                self.launch_line.render()
                self.figure.render()
                self.bat.render()
                self.barrier.render()

                # Render game info
                if self.__game_modifiers[self.bat.figures_knocked][0]:
                    GameInfo(
                        screen=self.screen,
                        position=(25, 500),
                        size=20,
                        text=f'Применен\nмодификатор:\n-----------------\n'
                             f'{names_of_modifiers[self.__game_modifiers[self.bat.figures_knocked][0]]}',
                        color=(13, 111, 131)
                    )

                GameInfo(self.screen, (25, 350), 60, text=str(self.bat.thrown_count).rjust(2, '0'))
                GameInfo(self.screen, (25, 415), 19, 'Брошено\nбит')

                GameInfo(self.screen, (-25, 350), 60, text=str(self.bat.figures_knocked).rjust(2, '0'))
                GameInfo(self.screen, (-25, 415), 19, 'Выбито\nфигур')

                if int(self.game_time) > 0:
                    text = f'Осталось времени: {self.game_time:.0f} сек.'
                else:
                    text = 'Игра закончена'

                GameInfo(
                    screen=self.screen,
                    position=(350, 730),
                    size=20,
                    text=f'Автобросок: {self.bat.auto_delay:.0f} сек. | Ctrl+P - пауза | Ctrl+M - меню',
                    color=(13, 111, 131),
                    is_center_pos=True
                )
                GameInfo(self.screen, (350, 760), 25, text, is_center_pos=True)

                # Level update
                if not len(parts_group):
                    if self.__can_create_particles:
                        create_particles((
                            self.figure.x + self.figure.field_width // 2,
                            self.figure.y + self.figure.field_height // 2
                        ))
                    self.__can_create_particles = False

                    if not self.bat.is_thrown:
                        self.__game_level += 1
                        self.bat.figures_knocked += 1
                        self.__can_create_particles = True

                        if self.__game_level <= 16:
                            self.next_level()
                        else:
                            self.__bonus_level_is_passed = True
                            self.stop()

                if self.bat.auto_delay <= 0:
                    self.bat.throw()

                # Render game effects
                apply_tv_scanlines(self.screen, self.effects_time)
                self.effects_time += 1

                # Display & Sprites update
                all_sprites.draw(self.screen)
                all_sprites.update()

                parts_group.draw(self.screen)

            pygame.display.update()
            self.clock.tick(GAME_FPS)

        self.main_window.game_stat_screen(self.game_stat)
