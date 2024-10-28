import re
from abc import ABC, abstractmethod
from random import randint
from typing import Optional

from shortuuid import uuid

from dmcli.utils import get_logger

command_logger = get_logger("command_logger")


class Command(ABC):
    def __init__(
        self,
        description: str,
        text: Optional[str] = None,
    ):
        self.text = text
        self.description = description
        self._id = uuid()

    @abstractmethod
    def run(self):
        pass


class Roll(Command):
    def __init__(self, text: Optional[str] = None):
        description = """
        Rolls 1d20 by default, otherwise rolls anyting in the format of
        XdY +/- Z
        """
        super().__init__(description=description, text=text)
        self.executed = False
        self.value = None

    def run(self):
        def _roll(dice_sides: int) -> int:
            return randint(1, dice_sides)

        if self.executed:
            command_logger.debug(
                f"Roll command {self._id} has already been "
                "executed, returning saved value"
            )
            return self.value
        else:
            command_logger.debug(f"Running Roll command {self._id}...")
            if self.text is None:
                out = _roll(20)
                self.executed = True
                self.value = out
                return out
            elif "+" in self.text:
                dice, bonus = self.text.split("+")
                bonus = int(bonus)
            elif "-" in self.text:
                dice, bonus = self.text.split("-")
                bonus = int(bonus) * -1

            dice_count, dice_sides = re.split("[dD]", dice)
            if dice_count == "":
                dice_count = 1

            rolls = [randint(1, int(dice_sides)) for _ in range(int(dice_count))]

            out = sum(rolls) + bonus
            self.value = out
            self.executed = True
            return out
