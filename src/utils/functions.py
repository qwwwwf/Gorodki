import random
from src.utils import ModEnum

def generate_game_modifiers() -> list[tuple[int, int | float | None, int | None]]:
    game_modifiers = random.choices(list(range(10)), weights=[55, 5, 5, 5, 5, 5, 5, 5, 5, 5], k=16)

    for i in range(len(game_modifiers)):
        match game_modifiers[i]:
            case ModEnum.BOOST.value:
                game_modifiers[i] = game_modifiers[i], round(random.uniform(1.05, 1.8), 2), random.randint(0, 1)

            case ModEnum.BAT_IS_EXPLOSIVE.value:
                game_modifiers[i] = game_modifiers[i], round(random.uniform(1.05, 1.8), 2), random.randint(0, 1)

            case ModEnum.BAT_HAS_ANGULAR_MOVEMENT.value:
                game_modifiers[i] = game_modifiers[i], random.randint(120, 45)

            case ModEnum.BAT_EXTENSION.value:
                game_modifiers[i] = game_modifiers[i], round(random.uniform(0.8, 1.4), 2)

            case ModEnum.INCREASE_GAME_TIME.value:
                game_modifiers[i] = game_modifiers[i], round(random.uniform(1.2, 1.5), 2)

            case ModEnum.DECREASE_GAME_TIME.value:
                game_modifiers[i] = game_modifiers[i], round(random.uniform(1.5, 2), 2)

            case ModEnum.SLOWDOWN.value | ModEnum.BARRIER.value | ModEnum.UNCHANGEABLE_LAUNCH_LINE.value:
                game_modifiers[i] = game_modifiers[i],

    return game_modifiers


def parse_game_modifiers(modifiers_list: list, level: int) -> dict:
    level -= 1
    game_modifiers = {
        'bat_boost': 1,
        'figure_boost': 1,
        'bat_is_explosive': False,
        'bat_has_angular_movement': 90,
        'bat_extension': 1,
        'increase_game_time': 1,
        'barrier': False,
        'unchangeable_launch_line': False
    }

    match modifiers_list[level][0]:
        case ModEnum.BOOST.value | ModEnum.SLOWDOWN.value:
            game_modifiers[f'{"figure" if modifiers_list[level][2] else "bat"}_boost'] = modifiers_list[level][1]

        case ModEnum.BAT_IS_EXPLOSIVE.value:
            game_modifiers['bat_is_explosive'] = True

        case ModEnum.BAT_HAS_ANGULAR_MOVEMENT.value:
            game_modifiers['bat_has_angular_movement'] = modifiers_list[level][1]

        case ModEnum.BAT_EXTENSION.value:
            game_modifiers['bat_extension'] = modifiers_list[level][1]

        case ModEnum.INCREASE_GAME_TIME.value | ModEnum.DECREASE_GAME_TIME.value:
            game_modifiers['increase_game_time']= modifiers_list[level][1]

        case ModEnum.BARRIER.value:
            game_modifiers['barrier'] = True

    return game_modifiers
