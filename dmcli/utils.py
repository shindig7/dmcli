import logging
from math import floor
from typing import Any, Dict, Tuple


def get_logger(name: str, level: int = 20) -> logging.Logger:
    FORMAT = "[%(asctime)s] - [%(levelname)s] - [%(funcName)s] - %(message)s"
    logging.basicConfig(level=level, format=FORMAT)
    return logging.getLogger(name)


def argparse(command: str) -> Tuple[str, Dict[str, Any]]:
    func, args = command.split(" ", 1)
    out_args = []
    for arg in args.split(" "):
        if "," in arg:
            out_args.append(arg.split(","))
        else:
            out_args.append(arg)
    return tuple([func] + out_args)


def halved(amount: int) -> int:
    return floor(amount / 2)
