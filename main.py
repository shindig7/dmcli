from rich.console import Console

from dmcli.roll import roll
from dmcli.utils import argparse

DEBUG_MODE = False


def run_command(func: str, args: str) -> None:
    command_options = {
        "roll": roll,
        "set": change_setting,
    }
    try:
        command_options[func](args)
    except KeyError:
        print("!!! COMMAND NOT RECOGNIZED !!!")


def change_setting(change: str) -> None:
    global DEBUG_MODE
    setting, value = change.split("=")
    if setting == "debug":
        DEBUG_MODE = eval(value.capitalize())


if __name__ == "__main__":
    console = Console()
    previous_command = ""

    while True:
        try:
            command = input(">>> ")
            if command == "exit":
                break
            elif command == "":
                if previous_command != "":
                    run_command(*previous_command)
            else:
                func, args = argparse(command)
                run_command(func, args)
                previous_command = (func, args)
        except Exception as e:
            if DEBUG_MODE:
                console.print_exception(show_locals=True)
            else:
                console.print(e)
