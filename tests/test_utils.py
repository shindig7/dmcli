from src.utils import argparse, halved


def test_argparse() -> None:
    command = "roll 1d20"
    x_command = "stat perception Ket"
    xx_command = "stat perception Ket,Morthos"

    assert argparse(command) == ("roll", "1d20")
    assert argparse(x_command) == ("stat", "perception", "Ket")
    assert argparse(xx_command) == ("stat", "perception", ["Ket", "Morthos"])


def test_halved():
    assert halved(10) == 5
    assert halved(11) == 5
