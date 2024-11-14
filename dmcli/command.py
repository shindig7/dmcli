import random
import re
from abc import ABC, abstractmethod
from pathlib import Path

import rich

from dmcli.session import Session
from dmcli.utils import strip_split


class Command(ABC):
    def __init__(self, description: str):
        self.description = description

    @abstractmethod
    def execute(self, args, input_data=None):
        raise NotImplementedError


class Roll(Command):
    def __init__(self):
        description = """Rolls 1d20 by default, otherwise rolls anything in the format of XdY +/- Z"""
        self.system_random = random.SystemRandom()
        super().__init__(description)

    def execute(self, args, input_data=None):
        try:
            dice_combo = args[0]
        except IndexError:
            return self.execute(["1d20"])
        else:
            if "+" in dice_combo:
                dice, bonus = strip_split(dice_combo, "+")
                bonus = int(bonus)
            elif "-" in dice_combo:
                dice, bonus = strip_split(dice_combo, "-")
                bonus = int(bonus) * -1
            else:
                dice, bonus = dice_combo, 0

            dice_count, dice_sides = re.split("[dD]", dice)
            if dice_count == "":
                dice_count = 1

            rolls = []
            for _ in range(int(dice_count)):
                rolls.append(self.system_random.randint(1, int(dice_sides)))

            rich.print(sum(rolls) + bonus, str(rolls))
            return sum(rolls) + bonus


class AbilityCheck(Command):
    def __init__(self):
        description = """Rolls a d20 and adds the ability modifier to it"""
        super().__init__(description)

    def execute(self, args, input_data=None):
        try:
            bonus = int(args[0])
        except IndexError:
            bonus = int(input_data)
        return Roll().execute(["1d20"]) + bonus


class LoadCharacter(Command):
    def __init__(self, session: Session):
        description = """Loads a character from a file"""
        self.session = session
        super().__init__(description)

    def execute(self, args, input_data=None):
        self.session.load_character(Path(args[0]))


class SaveSession(Command):
    def __init__(self, session: Session):
        description = """Saves the current session to a file"""
        self.session = session
        super().__init__(description)

    def execute(self, args, input_data=None):
        self.session.save_session()


class NameSession(Command):
    def __init__(self, session: Session):
        description = """Names the current session"""
        self.session = session
        super().__init__(description)

    def execute(self, args, input_data=None):
        self.session.name_session(args[0])
