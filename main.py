import shlex

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from rich.console import Console

from dmcli.roll import roll

DEBUG_MODE = True


def run_command(func: str, args: str) -> None:
    command_options = {
        "roll": roll,
    }
    try:
        command_options[func](args)
    except KeyError:
        print("!!! COMMAND NOT RECOGNIZED !!!")


"""
class DMCLI(cmd.Cmd):
    prompt = ">>> "
    intro = "Welcome to the DM CLI. Type 'help' for a list of commands."

    def do_roll(self, arg):
        roll(arg)

    def do_quit(self, arg):
        print("Goodbye!")
        return True
"""


class Command:
    def execute(self, args, input_data=None):
        raise NotImplementedError


class Roll(Command):
    def execute(self, args, input_data=None):
        return roll(args)


class Uppercase(Command):
    def execute(self, args, input_data=None):
        text = " ".join(args) if args else input_data
        return str(text).upper()


class Echo(Command):
    def execute(self, args, input_data=None):
        return " ".join(args)


class DMCLI:
    def __init__(self):
        self.console = Console()
        self.commands = {
            "roll": Roll(),
            "echo": Echo(),
            "uppercase": Uppercase(),
        }
        self.completer = WordCompleter(list(self.commands.keys()) + ["exit"])
        self.session = PromptSession(
            history=FileHistory(".dmcli_history"), completer=self.completer
        )

    def execute_command(self, command, args, input_data=None):
        if command in self.commands:
            return self.commands[command].execute(args, input_data)
        else:
            return f"Unknown command: {command}"

    def execute_pipeline(self, pipeline):
        input_data = None
        for command, args in pipeline:
            output = self.execute_command(command, args, input_data)
            input_data = output
        return input_data

    def parse_pipeline(self, line):
        commands = [cmd.strip() for cmd in line.split("|")]
        pipeline = []
        for cmd in commands:
            parts = shlex.split(cmd)
            pipeline.append((parts[0], parts[1:]))
        return pipeline

    def run(self):
        while True:
            try:
                line = self.session.prompt(">>> ")
                if line.lower() == "exit":
                    break
                pipeline = self.parse_pipeline(line)
                result = self.execute_pipeline(pipeline)
                self.console.print(result)
            except KeyboardInterrupt:
                break
            except EOFError:
                break
            except Exception as e:
                if DEBUG_MODE:
                    self.console.print_exception(show_locals=True)
                else:
                    self.console.print(e)
        self.console.print("Goodbye!")


if __name__ == "__main__":
    # console = Console()
    DMCLI().run()
    """
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
    """
