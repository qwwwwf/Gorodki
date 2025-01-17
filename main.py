import pygame

from src.utils import *
from src.objects import *
from src.components.effects import apply_tv_scanlines, create_particles


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Городки')

        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()

        # Game stats
        self.bat_thrown = 0
        self.figures_knocked = 0
        self.time = 120

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()

    # TODO: разбить основной код игры на отдельные файлы и функции
    def run(self):
        # Init game objects
        launch_line = LaunchLine(self.screen)
        figure = Figure(self.screen, 'figure1.txt')
        bat = Bat(self.screen)

        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.terminate()

                    case pygame.K_SPACE:
                        bat.thrown()

                    # Если клавиша зажата
                    case pygame.KEYDOWN:
                        ctrl_pressed = pygame.key.get_mods() & pygame.KMOD_CTRL

                        if ctrl_pressed and event.key == pygame.K_q:
                            print('TEST')
                        else:
                            match event.key:
                                case pygame.K_LEFT:
                                    bat.is_moving = True
                                    bat.is_right_move = False

                                case pygame.K_RIGHT:
                                    bat.is_moving = True
                                    bat.is_right_move = True

                    # Если клавиша отжата
                    case pygame.KEYUP:
                        bat.is_moving = False

                    # TEST
                    case pygame.MOUSEBUTTONDOWN:
                        create_particles(pygame.mouse.get_pos())

            self.screen.fill(BLUE)
            self.time -= 1 / GAME_FPS
            bat.auto_delay -= 1 / GAME_FPS

            # Rendering objects
            launch_line.render()
            figure.render()
            bat.render()

            # Game info
            GameInfo(self.screen, 25, 350, 60, text=str(self.figures_knocked).ljust(2, '0'))
            GameInfo(self.screen, 25, 415, 19, 'Брошено\nбит')

            GameInfo(self.screen, -25, 350, 60, text=str(self.bat_thrown).ljust(2, '0'))
            GameInfo(self.screen, -25, 415, 19, 'Выбито\nфигур')

            if int(self.time) > 0:
                GameInfo(self.screen, 175, 750, 25, f'Осталось времени: {self.time:.0f} сек.')
            else:
                GameInfo(self.screen, 245, 750, 25, 'Игра закончена')

            if bat.auto_delay <= 0:
                self.time = 0

            # Rendering effects
            apply_tv_scanlines(self.screen, self.time)

            # Display & Sprites update
            parts_group.draw(self.screen)
            all_sprites.draw(self.screen)
            all_sprites.update()

            pygame.display.update()
            self.clock.tick(GAME_FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
