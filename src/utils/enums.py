from enum import Enum


class ModEnum(Enum):
    # Bat & Figure
    BOOST = 1
    SLOWDOWN = 2
    BAT_IS_EXPLOSIVE = 3
    BAT_HAS_ANGULAR_MOVEMENT = 4

    # Game's field
    BARRIER = 5

    # Game
    INCREASE_GAME_TIME = 6
    DECREASE_GAME_TIME = 7

    # Launch line
    UNCHANGEABLE_LAUNCH_LINE = 8
    __Nothing = 9


class SideEnum(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
