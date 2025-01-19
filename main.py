from src.utils import *
from src.objects import *
from src.components.game_screen import Game


class MainWindow:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Городки')

        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()

        self.start()

    @staticmethod
    def terminate():
        pygame.quit()
        sys.exit()

    def start(self):
        Game(self)


if __name__ == '__main__':
    MainWindow()
