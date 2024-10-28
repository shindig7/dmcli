from dmcli.character import NPC, PC, Character, create_from_json
from dmcli.special_types import DamageType, DClass, Race


def test_npc():
    vamp = NPC(
        nickname="vamp1",
        name="Vampire",
        health=120,
        ac=18,
        immunities=[DamageType.BLUDGEONING],
        resistances=[DamageType.PIERCING],
    )

    vamp.heal(20)
    assert vamp.health == 140

    vamp.take_damage(dmg_amount=20, dmg_type=DamageType.NECROTIC)
    assert vamp.health == 120

    vamp.take_damage(dmg_amount=20, dmg_type=DamageType.PIERCING)
    assert vamp.health == 110

    vamp.take_damage(dmg_amount=20, dmg_type=DamageType.BLUDGEONING)
    assert vamp.health == 110


def test_pc():
    grendor = PC(
        name="Grendor Herlsson",
        dnd_class=DClass.FIGHTER,
        race=Race.HUMAN,
        health=120,
        ac=18,
        immunities=[DamageType.BLUDGEONING],
        resistances=[DamageType.PIERCING],
    )

    grendor.heal(20)
    assert grendor.health == 140

    grendor.take_damage(dmg_amount=20, dmg_type=DamageType.NECROTIC)
    assert grendor.health == 120

    grendor.take_damage(dmg_amount=20, dmg_type=DamageType.PIERCING)
    assert grendor.health == 110

    grendor.take_damage(dmg_amount=20, dmg_type=DamageType.BLUDGEONING)
    assert grendor.health == 110


def test_create_from_json():
    test_npc = {
        "type": "NPC",
        "nickname": "vamp1",
        "name": "Vampire",
        "health": 120,
        "ac": 18,
        "immunities": ["bludgeoning"],
        "resistances": ["piercing"],
    }

    vamp = create_from_json(test_npc)

    test_pc = {
        "type": "PC",
        "name": "Grendor Herlsson",
        "dnd_class": "fighter",
        "race": "human",
        "health": 120,
        "ac": 18,
        "immunities": ["bludgeoning"],
        "resistances": ["piercing"],
    }

    grendor = create_from_json(test_pc)
