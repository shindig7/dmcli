import pytest
from pydantic import ValidationError
from dmcli.special_types import DamageType, DClass, Gender, Race
from dmcli.utils import halved

@pytest.fixture
def mock_character_data():
    return {
        "name": "Test Character",
        "nickname": "Tester",
        "race": "elf",
        "gender": "female",
    }

@pytest.fixture
def mock_combatant_data(mock_character_data):
    return {
        **mock_character_data,
        "max_hp": 100,
        "current_hp": 100,
        "ac": 15,
        "speed": 30,
        "defenses": {"immunities": ["acid"], "resistances": ["bludgeoning"]},
    }

@pytest.fixture
def mock_pc_data(mock_combatant_data):
    return {
        **mock_combatant_data,
        "dnd_class": "rogue",
        "temp_hp": 10,
        "ability_scores": {"strength": 10, "dexterity": 12},
        "proficiencies": {"weapons": ["sword"], "skills": ["acrobatics"]},
        "level": 5,
    }

def test_character_creation(mock_character_data):
    from dmcli.character import Character
    character = Character(**mock_character_data)
    assert character.name == "Test Character"
    assert character.nickname == "Tester"

def test_character_creation_from_json(mock_character_data):
    from dmcli.character import Character
    character = Character.create_from_json(mock_character_data)
    assert character.name == "Test Character"
    assert character.nickname == "Tester"

def test_combatant_creation(mock_combatant_data):
    from dmcli.character import Combatant
    combatant = Combatant(**mock_combatant_data)
    assert combatant.max_hp == 100
    assert combatant.ac == 15

def test_combatant_take_damage(mock_combatant_data, monkeypatch):
    from dmcli.character import Combatant
    monkeypatch.setattr("dmcli.utils.halved", halved)
    combatant = Combatant(**mock_combatant_data)
    combatant.take_damage(20, DamageType.ACID, magical=False)
    assert combatant.current_hp == 100  # Immune

    combatant.defenses["immunities"] = []
    combatant.take_damage(20, DamageType.BLUDGEONING, magical=False)
    assert combatant.current_hp == 90  # Resistant (halved to 10)

def test_combatant_healing(mock_combatant_data):
    from dmcli.character import Combatant
    combatant = Combatant(**mock_combatant_data)
    combatant.current_hp = 50
    combatant.heal(20)
    assert combatant.current_hp == 70

def test_pc_creation(mock_pc_data):
    from dmcli.character import PC
    pc = PC(**mock_pc_data)
    assert pc.level == 5
    assert pc.temp_hp == 10
    assert pc.proficiencies["weapons"] == ["sword"]

def test_pc_render(mock_pc_data, monkeypatch):
    from dmcli.character import PC
    from rich.console import Console

    class MockRenderPC:
        def __call__(self, pc, console):
            assert pc.name == "Test Character"
            assert isinstance(console, Console)

    monkeypatch.setattr("dmcli.render.render_pc", MockRenderPC())
    pc = PC(**mock_pc_data)
    pc.render(Console())

def test_invalid_ac_in_combatant(mock_combatant_data):
    from dmcli.character import Combatant
    mock_combatant_data["ac"] = -1
    with pytest.raises(ValidationError):
        Combatant(**mock_combatant_data)

def test_invalid_level_in_pc(mock_pc_data):
    from dmcli.character import PC
    mock_pc_data["level"] = 0
    with pytest.raises(ValidationError):
        PC(**mock_pc_data)
