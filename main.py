from src.utils import *
from src.objects import *
from src.components.effects import apply_tv_scanlines


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Городки')

        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        self.time = 0

        self.settings = {}

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()

    # TODO: разбить основной код игры на отдельные файлы и функции
    def run(self):
        # Init objects
        figure = Figure(self.screen, 'figure1.txt')
        launch_line = LaunchLine(self.screen)
        time = 20

        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        self.terminate()

                    case pygame.K_SPACE:
                        pass

                    # Если клавиша зажата
                    case pygame.KEYDOWN:
                        ctrl_pressed = pygame.key.get_mods() & pygame.KMOD_CTRL

                        if ctrl_pressed and event.key == pygame.K_q:
                            print('TEST')

                    # Если клавиша отжата
                    case pygame.KEYUP:
                        pass

            self.screen.fill(BLUE)
            time -= 1 / GAME_FPS

            # Rendering objects
            launch_line.render()
            figure.render()

            # Score
            GameInfo(self.screen, 25, 350, 60, text='00')
            GameInfo(self.screen, 25, 415, 18, 'Брошено\nбит')

            GameInfo(self.screen, -25, 350, 60, text='00')
            GameInfo(self.screen, -25, 415, 18, 'Выбито\nфигур')

            if int(time) > 0:
                GameInfo(self.screen, 175, 750, 25, f'Осталось времени: {time:.0f} сек.')
            else:
                GameInfo(self.screen, 245, 750, 25, 'Игра закончена')

            # Rendering effects
            apply_tv_scanlines(self.screen, self.time)

            # Display update
            parts_group.draw(self.screen)
            pygame.display.update()
            self.clock.tick(GAME_FPS)

            self.time += 1


if __name__ == '__main__':
    game = Game()
    game.run()
