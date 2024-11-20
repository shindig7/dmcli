from enum import Enum


class DClass(str, Enum):
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


class Race(str, Enum):
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


class DamageType(str, Enum):
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


class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NONBINARY = "nonbinary"

class AbilityScore(str, Enum):
    STRENGTH = "strength"
    DEXTERITY = "dexterity"
    CONSTITUTION = "constitution"
    INTELLIGENCE = "intelligence"
    WISDOM = "wisdom"
    CHARISMA = "charisma"

    def __init__(self, *args):
        short_name_dict = {
            "strength": "STR",
            "dexterity": "DEX",
            "constitution": "CON",
            "intelligence": "INT",
            "wisdom": "WIS",
            "charisma": "CHA",
        }
        self.short_name = short_name_dict[self.value]

class Skill(str, Enum):
    ACROBATICS = "acrobatics"
    ANIMAL_HANDLING = "animal handling"
    ARCANA = "arcana"
    ATHLETICS = "athletics"
    DECEPTION = "deception"
    HISTORY = "history"
    INSIGHT = "insight"
    INTIMIDATION = "intimidation"
    INVESTIGATION = "investigation"
    MEDICINE = "medicine"
    NATURE = "nature"
    PERCEPTION = "perception"
    PERFORMANCE = "performance"
    PERSUAISION = "persuasion"
    RELIGION = "religion"
    SLEIGHT_OF_HAND = "sleight of hand"
    STEALTH = "stealth"
    SURVIVAL = "survival"

    def __init__(self, *args):
        mod_type_dict = {
            "acrobatics": AbilityScore.DEXTERITY,
            "animal handling": AbilityScore.WISDOM,
            "arcana": AbilityScore.INTELLIGENCE,
            "athletics": AbilityScore.STRENGTH,
            "deception": AbilityScore.CHARISMA,
            "history": AbilityScore.INTELLIGENCE,
            "insight": AbilityScore.WISDOM,
            "intimidation": AbilityScore.CHARISMA,
            "investigation": AbilityScore.INTELLIGENCE,
            "medicine": AbilityScore.WISDOM,
            "nature": AbilityScore.INTELLIGENCE,
            "perception": AbilityScore.WISDOM,
            "performance": AbilityScore.CHARISMA,
            "persuasion": AbilityScore.CHARISMA,
            "religion": AbilityScore.INTELLIGENCE,
            "sleight of hand": AbilityScore.DEXTERITY,
            "stealth": AbilityScore.DEXTERITY,
            "survival": AbilityScore.WISDOM,
        }
        self.mod_type = mod_type_dict[self.value]