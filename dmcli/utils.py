from math import floor
from typing import Any, Dict, Tuple


def argparse(command: str) -> Tuple[str, Dict[str, Any]]:
    func, args = command.split(" ", 1)
    out_args = []
    for arg in args.split(" "):
        if "," in arg:
            out_args.append(arg.split(","))
        else:
            out_args.append(arg)
    return tuple([func] + out_args)


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
