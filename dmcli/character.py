from abc import ABC, abstractmethod
from enum import Enum
from numbers import Number
from typing import Dict, List, Union

from src.special_types import DamageType, DClass, Race, damage_dict
from src.utils import halved


class Character(ABC):
    def __init__(
        self,
        name: str,
        health: int,
        ac: int,
        immunities: List[DamageType],
        resistances: List[DamageType],
    ):
        self.name = name
        self.health = health
        self.AC = ac
        self.immunities = immunities
        self.resistances = resistances

    def take_damage(self, dmg_amount: int, dmg_type: DamageType, magical: bool = False):
        if dmg_type not in self.immunities:
            if dmg_type not in self.resistances:
                self.health -= dmg_amount
            else:
                self.health -= halved(dmg_amount)
        else:
            print("Immunity bitch")

    def heal(self, heal_amount: int):
        self.health += heal_amount


class NPC(Character):
    def __init__(
        self,
        nickname: str,
        name: str,
        health: int,
        ac: int,
        immunities: List[DamageType],
        resistances: List[DamageType],
    ):
        super().__init__(
            name,
            health,
            ac,
            immunities,
            resistances,
        )
        self.nickname = nickname


class PC(Character):
    def __init__(
        self,
        name: str,
        dnd_class: DClass,
        race: Race,
        health: int,
        ac: int,
        immunities: List[DamageType],
        resistances: List[DamageType],
    ):
        super().__init__(
            name,
            health,
            ac,
            immunities,
            resistances,
        )
        self.dnd_class = dnd_class
        self.race = race


def create_from_json(config: Dict[str, Union[str, Number]]) -> Union[NPC, PC]:
    if config["type"] == "NPC":
        immunities = [damage_dict.get(x) for x in config["immunities"]]
        resistances = [damage_dict.get(x) for x in config["resistances"]]
        return NPC(
            name=config["name"],
            nickname=config["nickname"],
            health=config["health"],
            ac=config["ac"],
            immunities=immunities,
            resistances=resistances,
        )
    elif config["type"] == "PC":
        immunities = [damage_dict.get(x) for x in config["immunities"]]
        resistances = [damage_dict.get(x) for x in config["resistances"]]
        return PC(
            name=config["name"],
            dnd_class=config["dnd_class"],
            race=config["race"],
            health=config["health"],
            ac=config["ac"],
            immunities=immunities,
            resistances=resistances,
        )
