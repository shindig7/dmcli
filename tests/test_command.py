from unittest.mock import MagicMock

import pytest

from dmcli.command import (
    AbilityCheck,
    Command,
    LoadCharacter,
    NameSession,
    Render,
    Roll,
    SaveSession,
    StatCheck,
)


def test_command_abstract():
    with pytest.raises(TypeError):
        Command("Base command description")


def test_roll_default():
    roll = Roll()
    result = roll.execute([])
    assert 1 <= result <= 20


def test_roll_complex(monkeypatch):
    roll = Roll()
    monkeypatch.setattr(
        roll.system_random, "randint", lambda a, b: 5
    )  # Mock roll to always return 5
    result = roll.execute(["2d6+3"])
    assert result == (5 + 5 + 3)  # Two rolls of 5 plus bonus


def test_roll_negative_bonus(monkeypatch):
    roll = Roll()
    monkeypatch.setattr(
        roll.system_random, "randint", lambda a, b: 10
    )  # Mock roll to always return 10
    result = roll.execute(["1d12-4"])
    assert result == (10 - 4)  # Roll minus bonus


def test_ability_check(monkeypatch):
    ability_check = AbilityCheck()
    monkeypatch.setattr(
        Roll, "execute", lambda self, args: 15
    )  # Mock roll result
    result = ability_check.execute(["2"])
    assert result == 17  # Roll result plus bonus


def test_load_character():
    mock_session = MagicMock()
    load_character = LoadCharacter(mock_session)
    load_character.execute(["data/grendor_herlsson.json"])
    mock_session.load_character.assert_called_once_with(
        "data/grendor_herlsson.json"
    )


def test_save_session():
    mock_session = MagicMock()
    save_session = SaveSession(mock_session)
    save_session.execute([])
    mock_session.save_session.assert_called_once()


def test_name_session():
    mock_session = MagicMock()
    name_session = NameSession(mock_session)
    name_session.execute(["Test Session"])
    mock_session.name_session.assert_called_once_with("Test Session")


def test_stat_check():
    mock_session = MagicMock()
    mock_character = MagicMock(strength=18)
    mock_session.pcs = {"Hero": mock_character}
    stat_check = StatCheck(mock_session)
    result = stat_check.execute(["Hero", "strength"])
    assert result == 18


def test_render(monkeypatch):
    mock_session = MagicMock()
    mock_console = MagicMock()
    mock_character = MagicMock()
    mock_session.pcs = {"Hero": mock_character}
    render_command = Render(mock_session, mock_console)
    render_command.execute(["Hero"])
    mock_character.render.assert_called_once_with(mock_console)
