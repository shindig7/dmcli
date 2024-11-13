import shlex

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from rich.console import Console

from dmcli.command import Roll, AbilityCheck

DEBUG_MODE = True

class DMCLI:
    def __init__(self):
        self.console = Console()
        self.commands = {
            "roll": Roll(),
            "ability": AbilityCheck(),
        }
        self.completer = WordCompleter(list(self.commands.keys()) + ["exit", "help"])
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

    def help_message(self):
        for command, obj in self.commands.items():
            self.console.print(f"[bold]{command}[/bold]: {obj.description}")

    def run(self):
        while True:
            try:
                line = self.session.prompt(">>> ")
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