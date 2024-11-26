import shlex

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from result import Err, is_ok
from rich.console import Console

from dmcli.command import (
    AbilityCheck,
    Damage,
    Heal,
    LoadCharacter,
    LoadParty,
    NameSession,
    Render,
    Roll,
    SaveSession,
    StatCheck,
)
from dmcli.session import Session
from dmcli.special_types import DamageType

DEBUG_MODE = True


class DMCLI:
    def __init__(self):
        self.console = Console()
        self.session = Session()
        self.commands = {
            "roll": Roll(),
            "ability": AbilityCheck(),
            "load": LoadCharacter(self.session, self),
            "save": SaveSession(self.session),
            "name": NameSession(self.session),
            "stat": StatCheck(self.session),
            "render": Render(self.session, self.console),
            "damage": Damage(self.session),
            "heal": Heal(self.session),
            "load_party": LoadParty(self.session, self),
        }
        self.completer = WordCompleter(
            list(self.commands.keys()) + ["exit", "help"] + list(DamageType)
        )
        self.prompt_session = PromptSession(
            history=FileHistory(".dmcli_history"), completer=self.completer
        )

    def execute_command(self, command, args, input_data=None):
        if command in self.commands:
            return self.commands[command].execute(args, input_data)
        else:
            return f"Unknown command: {command}"

    def execute_pipeline(self, pipeline):
        try:
            input_data = None
            for command, args in pipeline:
                output = self.execute_command(command, args, input_data)
                if is_ok(output):
                    input_data = output.ok_value
                else:
                    return output
            return input_data
        except Exception as e:
            if DEBUG_MODE:
                self.console.print_exception(show_locals=True)
            return Err(e)

    def parse_pipeline(self, line):
        commands = [cmd.strip() for cmd in line.split("|")]
        pipeline = []
        for cmd in commands:
            parts = shlex.split(cmd)
            pipeline.append((parts[0], parts[1:]))
        return pipeline

    def help_message(self):
        for command, obj in self.commands.items():
            self.console.print(f"[bold]{command}[/bold]: {obj.description}")

    def run(self):
        while True:
            try:
                line = self.prompt_session.prompt(">>> ")
                if line.lower() == "exit":
                    break
                elif line.lower() == "help":
                    self.help_message()
                    continue
                pipeline = self.parse_pipeline(line)
                result = self.execute_pipeline(pipeline)
                self.console.print(f"Result: {result}")
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
