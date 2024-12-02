from math import floor


def strip_split(string: str, sep: str) -> list[str]:
    return [x.strip() for x in string.split(sep)]


def halved(amount: int) -> int:
    return floor(amount / 2)


def get_proficiency_bonus(level: int) -> int:
    if level < 5:
        return 2
    elif level < 9:
        return 3
    elif level < 13:
        return 4
    elif level < 17:
        return 5
    else:
        return 6


def get_modifier(score: int) -> int:
    return floor((score - 10) / 2)
