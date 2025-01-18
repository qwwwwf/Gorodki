from enum import Enum


class ModEnum(Enum):
    # Bat & Figure
    BOOST = 1
    SLOWDOWN = 2
    BAT_IS_EXPLOSIVE = 3
    BAT_HAS_ANGULAR_MOVEMENT = 4
    BAT_EXTENSION = 5

    # Game's field
    BARRIER = 6

    # Game
    INCREASE_GAME_TIME = 7
    DECREASE_GAME_TIME = 8

    # Launch line
    UNCHANGEABLE_LAUNCH_LINE = 9
