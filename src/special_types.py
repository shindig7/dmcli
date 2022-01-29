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


class Race(Enum):
    ELF = "elf"
    HALF_ELF = "half-elf"
    HUMAN = "human"
    AASIMAR = "aasimar"


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
    "acid": DamageType.ACID,
    "bludgeoning": DamageType.BLUDGEONING,
    "cold": DamageType.COLD,
    "fire": DamageType.FIRE,
    "force": DamageType.FORCE,
    "lightning": DamageType.LIGHTNING,
    "necrotic": DamageType.NECROTIC,
    "piercing": DamageType.PIERCING,
    "psychic": DamageType.PSYCHIC,
    "radiant": DamageType.RADIANT,
    "slashing": DamageType.SLASHING,
    "thunder": DamageType.THUNDER,
}
