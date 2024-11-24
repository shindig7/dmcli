from pydantic import BaseModel, Field
from rich.console import Console

from dmcli.render import render_pc
from dmcli.special_types import (
    AbilityScore,
    DamageType,
    DClass,
    Gender,
    Race,
    Size,
)
from dmcli.utils import halved


class Character(BaseModel):
    name: str | None
    nickname: str
    race: Race
    gender: Gender

    @classmethod
    def create_from_json(cls, data):
        return cls(**data)


class Combatant(BaseModel):
    max_hp: int
    current_hp: int
    ac: int = Field(ge=0)
    speed: int
    ability_scores: dict[AbilityScore, int]
    defenses: dict[str, list[DamageType]]
    size: Size

    def take_damage(
        self, dmg_amount: int, dmg_type: DamageType, magical: bool = False
    ) -> int:
        if dmg_type in self.defenses.get("immunities", []):
            print(f"{self.name} is immune to {str(dmg_type)}!")
            return 0
        else:
            if dmg_type in self.defenses.get("resistances", []):
                dmg_amount = halved(dmg_amount)

            self.current_hp -= dmg_amount
            return dmg_amount

    def heal(self, heal_amount: int):
        if self.current_hp + heal_amount > self.max_hp:
            self.current_hp = self.max_hp
        else:
            self.current_hp += heal_amount

    def is_bloodied(self):
        return self.current_hp <= halved(self.max_hp)

    @property
    def hp(self):
        return f"{self.current_hp}/{self.max_hp}"

    @classmethod
    def create_from_json(cls, data):
        return cls(**data)


class NPC(Character):
    pass


class PC(Character, Combatant):
    dnd_class: DClass
    temp_hp: int
    proficiencies: dict[str, list[str]]
    level: int = Field(ge=1)
    languages: list[str]  # TODO: Enum
    senses: list[str]  # TODO: Enum

    def render(self, console: Console):
        render_pc(self, console)


class Monster(Combatant):
    name: str | None = None
    nickname: str
    challenge_rating: int
    traits: list[dict[str, str]]
    actions: list[dict[str, str]]
    equipment: list[str]


if __name__ == "__main__":
    console = Console()
    import json

    with open("data/bugbear.json", "r") as f:
        data = json.load(f)

    monster = Monster.create_from_json(data)
    console.print(monster.model_dump())
