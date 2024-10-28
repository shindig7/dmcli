from typing import Any, Dict, List, Optional, Type, Union

from command import Command


class Pipeline:
    def __init__(
        self,
        command_list: Optional[
            Union[List[Type[Command]], Dict[int, Type[Command]]]
        ] = None,
    ):
        self.commands = command_list

    def run(self, first_input: Any = None, verbose: bool = False):
        pass

    def add_command(self, command: Command) -> None:
        pass


if __name__ == "__main__":
    pipeline = Pipeline()
