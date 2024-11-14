# Dungeon Master CLI (DMCLI)

DMCLI is a command-line interface tool designed to assist Dungeon Masters (DMs) in managing and running tabletop RPG sessions. The CLI provides essential commands for rolling dice, managing characters, and tracking game sessions, making it a convenient tool for quick game actions and information handling.

## Features

- **Command Line Interface**: Intuitive commands for dice rolls, ability checks, and more.
- **Character Management**: Create and manage NPCs and PCs with attributes such as health, class, and race.
- **Session Tracking**: Organize and manage different sessions, load character data, and maintain session history.
- **Extensible Commands**: Easily add or modify commands with custom logic.

## Installation

Ensure you have Python installed on your system, then clone this repository and navigate to the project folder:

```bash
git clone <repository_url>
cd DMCLI
pip install -r requirements.txt
```

## Usage

To start DMCLI, run the following command:

```bash
python main.py
```

### Basic Commands

- **roll**: Rolls dice based on the format `XdY +/- Z`. Defaults to `1d20`.
- **ability**: Rolls a d20 and adds the ability modifier.

Use `help` in the CLI for a list of commands with descriptions.

### Character Management

Characters are defined as either NPCs or PCs, with attributes such as health, AC, immunities, and resistances. Character data can be loaded from JSON files into sessions for easy management.

### Session Management

Sessions allow you to manage the PCs and NPCs involved, with the ability to load character data from JSON files.

## Extending DMCLI

To add new commands, create a new class in `command.py` that inherits from `Command` and implement the `execute` method. Add the new command to the `DMCLI` command list in `main.py`.

## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request with your improvements or bug fixes.

--- 

This README should help others understand the purpose, usage, and structure of your project. Let me know if you'd like any additional sections!