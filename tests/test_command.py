from rich.console import Console

from dmcli.command import Command, Roll


def test_roll_command():
    roll = Roll()
    result = roll.run()
    assert result <= 20 and result >= 1

    damage = Roll("3d6 + 2").run()
    assert damage >= 5 and damage <= 20

    extreme_damage = Roll("8d6 + 8")
    d = extreme_damage.run()
    assert all(map(lambda k: k == d, [extreme_damage.run() for _ in range(10)]))


if __name__ == "__main__":
    console = Console()
    try:
        test_roll_command()
    except Exception as E:
        console.print_exception(show_locals=True)
