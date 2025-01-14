import pygame


class GameObject:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen

    def render(self):
        pass


class Bat(GameObject):
    def __init__(
            self,
            screen: pygame.Surface,
            speed: int | float = 10,
            angle_of_movement: int = 90,
            is_explosive: bool = False
    ):
        super().__init__(screen)

        self.__rps = 5
        self.speed = speed
        self.is_explosive = is_explosive
        self.angle_of_movement = angle_of_movement



class Figure(GameObject):
    def __init__(self, screen: pygame.Surface, speed: int | float = 15):
        super().__init__(screen)
        self.speed = speed


class LaunchLine(GameObject):
    def __init__(self, screen: pygame.Surface, y: int = 5):
        self.y = y
        super().__init__(screen)


class Barrier(GameObject):
    def __init__(self, screen: pygame.Surface, speed: int | float = 5):
        super().__init__(screen)
        self.speed = speed
