from enum import Enum


class DClass(Enum):
    ROGUE = "rogue"
    WIZARD = "wizard"
    SORCEROR = "sorceror"
    BARBARIAN = "barbarian"
    FIGHTER = "fighter"
    WARLOCK = "warlock"
    MONK = "monk"
    CLERIC = "cleric"
    RANGER = "ranger"
    BLOODHUNTER = "bloodhunter"
    ARTIFICER = "artificer"
    dclass_dict = {
        "rogue": ROGUE,
        "wizard": WIZARD,
        "sorceror": SORCEROR,
        "barbarian": BARBARIAN,
        "fighter": FIGHTER,
        "warlock": WARLOCK,
        "monk": MONK,
        "cleric": CLERIC,
        "ranger": RANGER,
        "bloodhunter": BLOODHUNTER,
        "artificer": ARTIFICER,
    }

    @classmethod
    def from_str(cls, class_str: str) -> "DamageType":
        try:
            return cls.damage_dict[class_str.lower()]
        except KeyError:
            raise KeyError(f"Invalid damage type: {class_str}")


class Race(Enum):
    AASIMAR = "aasimar"
    ELF = "elf"
    HALF_ELF = "half-elf"
    HALF_ORC = "half-orc"
    HALFLING = "halfling"
    HUMAN = "human"

    race_dict = {
        "aasimar": AASIMAR,
        "elf": ELF,
        "half-elf": HALF_ELF,
        "half-orc": HALF_ORC,
        "halfling": HALFLING,
        "human": HUMAN,
    }

    @classmethod
    def from_str(cls, race_str: str) -> "DamageType":
        try:
            return cls.race_dict[race_str.lower()]
        except KeyError:
            raise KeyError(f"Invalid damage type: {race_str}")


class DamageType(Enum):
    ACID = "acid"
    BLUDGEONING = "bludgeoning"
    COLD = "cold"
    FIRE = "fire"
    FORCE = "force"
    LIGHTNING = "lightning"
    NECROTIC = "necrotic"
    PIERCING = "piercing"
    PSYCHIC = "psychic"
    RADIANT = "radiant"
    SLASHING = "slashing"
    THUNDER = "thunder"
    damage_dict = {
        "acid": ACID,
        "bludgeoning": BLUDGEONING,
        "cold": COLD,
        "fire": FIRE,
        "force": FORCE,
        "lightning": LIGHTNING,
        "necrotic": NECROTIC,
        "piercing": PIERCING,
        "psychic": PSYCHIC,
        "radiant": RADIANT,
        "slashing": SLASHING,
        "thunder": THUNDER,
    }

    @classmethod
    def from_str(cls, dmg_str: str) -> "DamageType":
        try:
            return cls.damage_dict[dmg_str.lower()]
        except KeyError:
            raise KeyError(f"Invalid damage type: {dmg_str}")

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"
    NONBINARY = "nonbinary"

