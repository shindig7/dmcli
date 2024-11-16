import rich.repr
from abc import ABC
from rich.pretty import pprint
import json

from loguru import logger

from dmcli.special_types import DamageType, DClass, Race, Gender
from dmcli.utils import halved


class Character(ABC):
    def __init__(
        self,
        name: str,
        nickname: str,
        race: Race,
        gender: Gender,
    ):
        self.name = name
        self.nickname = nickname
        self.race = Race.from_str(race)
        self.gender = gender

    def to_dict(self) -> dict[str, int | float | str | DamageType]:
        return self.__dict__


class Combatant(Character):
    def __init__(
        self,
        name: str,
        nickname: str,
        race: Race,
        gender: Gender,
        max_hp: int,
        current_hp: int,
        ac: int,
        speed: int,
        defenses: dict[str, list[str]],
    ):
        self.max_hp = max_hp
        self.current_hp = current_hp
        self.ac = ac
        self.defenses = defenses
        self.speed = speed

        super().__init__(
            name,
            nickname,
            race,
            gender,
        )

    def take_damage(
        self, dmg_amount: int, dmg_type: DamageType, magical: bool = False
    ):
        if dmg_type in self.defenses.get("immunities", []):
            print(f"{self.name} is immune to {str(dmg_type)}!")
            return
        else:
            if dmg_type in self.defenses.get("resistances", []):
                dmg_amount = halved(dmg_amount)

            self.current_hp -= dmg_amount
            print(f"{self.name} takes {dmg_amount} {str(dmg_type)} damage!")

    def heal(self, heal_amount: int):
        self.health += heal_amount


class NPC(Character):
    def __init__(
        self,
        nickname: str,
        name: str,
        race: Race,
        gender: Gender,
    ):
        super().__init__(
            name,
            nickname,
            race,
            gender,
        )

    @staticmethod
    def create_from_json(data) -> "NPC":
        try:
            return NPC(**data)
        except TypeError as e:
            logger.error(f"Missing attribute: {e}")


@rich.repr.auto
class PC(Combatant):
    def __init__(
        self,
        name: str,
        nickname: str,
        level: int,
        race: Race,
        gender: Gender,
        dnd_class: DClass,
        max_hp: int,
        current_hp: int,
        temp_hp: int,
        ac: int,
        speed: int,
        ability_scores: dict[str, int],
        proficiencies: dict[str, list[str]],
        defenses: dict[str, list[str]],
    ):
        self.dnd_class = DClass.from_str(dnd_class)
        self.level = level
        self.temp_hp = temp_hp
        self.ability_scores = ability_scores
        self.proficiencies = proficiencies
        super().__init__(
            name,
            nickname,
            race,
            gender,
            max_hp,
            current_hp,
            ac,
            speed,
            defenses,
        )

    @staticmethod
    def create_from_json(data) -> "PC":
        try:
            data.pop("type")
            return PC(**data)
        except TypeError as e:
            logger.error(f"Missing attribute: {e}")


if __name__ == "__main__":
    with open("data/grendor_herlsson.json", "r") as f:
        data = json.load(f)
    pc = PC.create_from_json(data)
    pprint(pc)
