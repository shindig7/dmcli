from typing import TYPE_CHECKING

from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from dmcli.utils import get_modifier

if TYPE_CHECKING:
    from dmcli.character import PC


def render_pc(pc: "PC", console: Console):
    console.print(
        Panel(f"[bold green]{pc.name}[/bold green]"), justify="center"
    )
    columns = Columns(expand=True)

    # Basic Info
    basic_info = Table(expand=True, box=box.ROUNDED)
    basic_info.add_column("Details")
    basic_info.add_column("Value")

    basic_info.add_row("Nickname", pc.nickname)
    basic_info.add_row("Race", pc.race.capitalize())
    basic_info.add_row("Class", pc.dnd_class.capitalize())
    basic_info.add_row("Level", str(pc.level))
    basic_info.add_row("Gender", pc.gender.capitalize())

    columns.add_renderable(basic_info)

    # Ability Scores
    ability_scores = Table(expand=True, box=box.ROUNDED)
    ability_scores.add_column("Ability")
    ability_scores.add_column("Score")
    ability_scores.add_column("Modifier")

    for ability, score in pc.ability_scores.items():
        ability_scores.add_row(
            ability.upper(), str(score), str(get_modifier(score))
        )

    columns.add_renderable(ability_scores)

    console.print(columns)


if __name__ == "__main__":
    import json

    console = Console()

    with open("data/grendor_herlsson.json", "r") as f:
        pc = PC.create_from_json(json.load(f))
    render_pc(pc, console)
