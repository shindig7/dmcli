from loguru import logger
from pydantic import BaseModel, Field
from rich.pretty import pprint

from dmcli.special_types import DamageType, DClass, Gender, Race
from dmcli.utils import halved


class Character(BaseModel):
    name: str
    nickname: str
    race: Race
    gender: Gender

    @classmethod
    def create_from_json(cls, data):
        return cls(**data)


class Combatant(Character):
    max_hp: int
    current_hp: int
    ac: int = Field(ge=0)
    speed: int
    defenses: dict[str, list[str]]

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
    pass


class PC(Combatant):
    dnd_class: DClass
    temp_hp: int
    ability_scores: dict[str, int]
    proficiencies: dict[str, list[str]]
    level: int = Field(ge=1)
