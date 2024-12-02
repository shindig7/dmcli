import random
import re
from abc import ABC, abstractmethod
from pathlib import Path

import rich
from prompt_toolkit import PromptSession
from result import Err, Ok
from rich.console import Console

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
            return Ok(self.execute(["1d20"]))
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
            return Ok(sum(rolls) + bonus)


class AbilityCheck(Command):
    def __init__(self):
        description = """Rolls a d20 and adds the ability modifier to it"""
        super().__init__(description)

    def execute(self, args, input_data=None):
        try:
            bonus = int(args[0])
        except IndexError:
            bonus = int(input_data)
        if bonus >= 0:
            return Roll().execute([f"1d20 + {bonus}"])
        else:
            return Roll().execute([f"1d20 - {bonus}"])


class LoadCharacter(Command):
    def __init__(self, session: Session, prompt_session: PromptSession):
        description = """Loads a character from a file"""
        self.session = session
        self.prompt_session = prompt_session
        super().__init__(description)

    def execute(self, args, input_data=None):
        self.session.load_character(Path(args[0]))
        self.prompt_session.completer.words += list(self.session.pcs.keys())
        return Ok("Character loaded")


class SaveSession(Command):
    def __init__(self, session: Session):
        description = """Saves the current session to a file"""
        self.session = session
        super().__init__(description)

    def execute(self, args, input_data=None):
        self.session.save_session()
        return Ok("Session saved")


class NameSession(Command):
    def __init__(self, session: Session):
        description = """Names the current session"""
        self.session = session
        super().__init__(description)

    def execute(self, args, input_data=None):
        self.session.name_session(args[0])
        return Ok("Session named")


class StatCheck(Command):
    def __init__(self, session: Session):
        description = """Shows a character's stats"""
        self.session = session
        super().__init__(description)

    def execute(self, args, input_data=None):
        character, get_stat = args
        character = self.session.pcs.get(
            character, self.session.npcs.get(character)
        )
        if character is None:
            return Err(f"Character {character} not found")
        try:
            character_stat = getattr(character, get_stat)
            return Ok(character_stat)
        except AttributeError:
            return Err(f"Stat {get_stat} not found")


class Render(Command):
    def __init__(self, session: Session, console: Console):
        description = """Renders a character"""
        self.session = session
        self.console = console
        super().__init__(description)

    def execute(self, args, input_data=None):
        character = self.session.pcs.get(
            args[0], self.session.npcs.get(args[0])
        )
        character.render(self.console)
        return Ok(f"{character.name} rendered")


class Damage(Command):
    def __init__(self, session: Session):
        description = """Deals damage to a character"""
        self.session = session
        super().__init__(description)

    def execute(self, args, input_data=None):
        character, dmg_amount, dmg_type = args
        character = self.session.pcs.get(
            character, self.session.npcs.get(character)
        )
        true_dmg = character.take_damage(int(dmg_amount), dmg_type)
        return Ok(f"{character.name} took {true_dmg} {dmg_type} damage")


class Heal(Command):
    def __init__(self, session: Session):
        description = """Heals a character"""
        self.session = session
        super().__init__(description)

    def execute(self, args, input_data=None):
        character, heal_amount = args
        character = self.session.pcs.get(
            character, self.session.npcs.get(character)
        )
        character.heal(int(heal_amount))
        return Ok(f"{character.name} healed {heal_amount}")


class LoadParty(Command):
    def __init__(self, session: Session, prompt_session: PromptSession):
        description = """Loads a party from a folder"""
        self.session = session
        self.prompt_session = prompt_session
        super().__init__(description)

    def execute(self, args, input_data=None):
        self.session.load_party(Path(args[0]))
        self.prompt_session.completer.words += list(self.session.pcs.keys())
        self.prompt_session.completer.words += list(self.session.npcs.keys())
        self.prompt_session.completer.words += list(
            self.session.monsters.keys()
        )
        return Ok("Party loaded")
