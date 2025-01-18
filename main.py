from src.utils import *
from src.objects import *
from src.components.effects import apply_tv_scanlines, create_particles


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Городки')

        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        self.effects_time = 0

        # Game edit
        self.__paused = False
        self.__can_create_particles = True

        # Game stats
        self.game_time = DEFAULT_GAME_TIME
        self.game_info = {
            'level': 1,
            'modifiers': []  # (id модификатора, значение модификатора), пример: (1, 1.05) - ускорение 1.05x
        }

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()

    def render_pause(self):
        darken_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        darken_surface.fill((0, 0, 0, 155))
        self.screen.blit(darken_surface, (0, 0))

    def stop(self):
        pass

    # TODO: разбить основной код игры на отдельные файлы и функции
    def run(self):
        # Initial game objects
        launch_line = LaunchLine(self.screen)
        figure = Figure(self.screen, f'figure{self.game_info["level"]}.txt')
        bat = Bat(self.screen)

        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.terminate()

                    # Если клавиша зажата
                    case pygame.KEYDOWN:
                        ctrl_pressed = pygame.key.get_mods() & pygame.KMOD_CTRL

                        if ctrl_pressed:
                            match event.key:
                                case pygame.K_q:
                                    self.terminate()

                                case pygame.K_p:
                                    self.__paused = not self.__paused
                                    self.render_pause()
                        else:
                            match event.key:
                                case pygame.K_LEFT:
                                    bat.is_moving = True
                                    bat.is_right_move = False

                                case pygame.K_RIGHT:
                                    bat.is_moving = True
                                    bat.is_right_move = True

                                case pygame.K_SPACE | pygame.K_UP:
                                    bat.throw()

                    # Если клавиша отжата
                    case pygame.KEYUP:
                        bat.is_moving = False

            if not self.__paused:
                self.screen.fill(BLUE)
                self.game_time -= 1 / GAME_FPS

                if not bat.is_thrown:
                    bat.auto_delay -= 1 / GAME_FPS

                # Render game objects
                launch_line.render()
                figure.render()
                bat.render()

                # Render game info
                GameInfo(self.screen, (25, 350), 60, text=str(bat.thrown_count).rjust(2, '0'))
                GameInfo(self.screen, (25, 415), 19, 'Брошено\nбит')

                GameInfo(self.screen, (-25, 350), 60, text=str(bat.figures_knocked).rjust(2, '0'))
                GameInfo(self.screen, (-25, 415), 19, 'Выбито\nфигур')

                if int(self.game_time) > 0:
                    text = f'Осталось времени: {self.game_time:.0f} сек.'
                else:
                    text = 'Игра закончена'

                GameInfo(
                    screen=self.screen,
                    position=(350, 730),
                    size=20,
                    text=f'Автобросок: {bat.auto_delay:.0f} сек. | Ctrl+P - пауза',
                    color=(13, 111, 131),
                    is_center_pos=True
                )
                GameInfo(self.screen, (350, 760), 25, text, is_center_pos=True)

                # Level update
                if not len(parts_group):
                    if self.__can_create_particles:
                        create_particles((WIDTH // 2, 200))
                    self.__can_create_particles = False

                    if not bat.is_thrown:
                        self.game_info['level'] += 1
                        bat.figures_knocked += 1
                        self.__can_create_particles = True

                        if self.game_info['level'] <= 16:
                            figure = Figure(self.screen, f'figure{self.game_info["level"]}.txt')
                        else:
                            self.terminate()  # TODO: завершение игры

                if not bat.is_thrown and bat.thrown_count >= 24:
                    pass

                if bat.auto_delay <= 0:
                    bat.throw()

                # Render game effects
                apply_tv_scanlines(self.screen, self.effects_time)
                self.effects_time += 1

                # Display & Sprites update
                all_sprites.draw(self.screen)
                all_sprites.update()

                parts_group.draw(self.screen)

            pygame.display.update()
            self.clock.tick(GAME_FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
