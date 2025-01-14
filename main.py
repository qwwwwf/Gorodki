import sys
import pygame
from src.utils.enums import *
from src.utils.constants import SIZE, GAME_FPS


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Городки')

        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()

        self.state = GameState.MENU
        self.settings = {}

    def run(self):
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    case _:
                        match self.state:
                            case GameState.MENU:
                                print('Menu')

                            case GameState.FIELD:
                                print('Field')

            pygame.display.update()
            self.clock.tick(GAME_FPS)


if __name__ == '__main__':
    game = Game()
    game.run()
