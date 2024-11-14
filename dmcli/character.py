from abc import ABC

from loguru import logger

from dmcli.special_types import DamageType, DClass, Race, damage_dict
from dmcli.utils import halved


class Character(ABC):
    def __init__(
        self,
        name: str,
        health: int,
        ac: int,
        immunities: list[DamageType],
        resistances: list[DamageType],
    ):
        self.name = name
        self.health = health
        self.AC = ac
        self.immunities = immunities
        self.resistances = resistances

    def take_damage(
        self, dmg_amount: int, dmg_type: DamageType, magical: bool = False
    ):
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
        immunities: list[DamageType],
        resistances: list[DamageType],
    ):
        super().__init__(
            name,
            health,
            ac,
            immunities,
            resistances,
        )
        self.nickname = nickname

    @staticmethod
    def create_from_json(data) -> "NPC":
        try:
            return NPC(
                name=data["name"],
                nickname=data["nickname"],
                health=data["health"],
                ac=data["ac"],
                immunities=data["immunities"],
                resistances=data["resistances"],
            )
        except KeyError as K:
            logger.error(f"Missing attribute: {K}")

    def to_dict(self) -> dict[str, int | float | str | DamageType]:
        return {
            "name": self.name,
            "nickname": self.nickname,
            "health": self.health,
            "ac": self.AC,
            "immunities": [x.name for x in self.immunities],
            "resistances": [x.name for x in self.resistances],
        }


class PC(Character):
    def __init__(
        self,
        name: str,
        dnd_class: DClass,
        race: Race,
        health: int,
        ac: int,
        immunities: list[DamageType],
        resistances: list[DamageType],
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

    @staticmethod
    def create_from_json(data) -> "PC":
        try:
            immunities = [damage_dict.get(x) for x in data["immunities"]]
            resistances = [damage_dict.get(x) for x in data["resistances"]]
            return PC(
                name=data["name"],
                dnd_class=data["dnd_class"],
                race=data["race"],
                health=data["health"],
                ac=data["ac"],
                immunities=immunities,
                resistances=resistances,
            )
        except KeyError as K:
            logger.error(f"Missing attribute: {K}")
