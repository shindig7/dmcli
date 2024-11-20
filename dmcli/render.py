from typing import TYPE_CHECKING

from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from dmcli.utils import get_modifier, get_proficiency_bonus, halved
from dmcli.special_types import Skill

if TYPE_CHECKING:
    from dmcli.character import PC


def render_pc(pc: "PC", console: Console):
    console.print(
        Panel(f"[bold green]{pc.name}[/bold green]"), justify="center"
    )
    columns = Columns(expand=True, padding=0)

    # Basic Info
    basic_info = Table(expand=True, box=box.ROUNDED)
    basic_info.add_column("Stat")
    basic_info.add_column("Value")

    basic_info.add_row("Nickname", pc.nickname)
    basic_info.add_row("Race", pc.race.capitalize())
    basic_info.add_row("Class", pc.dnd_class.capitalize())
    basic_info.add_row("Level", str(pc.level))
    basic_info.add_row("Gender", pc.gender.capitalize())
    basic_info.add_row("", "")

    columns.add_renderable(basic_info)

    # Misc Stats
    misc = Table(expand=True, box=box.ROUNDED)
    misc.add_column("Stat", justify="right")
    misc.add_column("Value", justify="center")

    misc.add_row("Max HP", str(pc.max_hp))
    if pc.current_hp <= halved(pc.max_hp):
        misc.add_row("Current HP", f"[red]{pc.current_hp}[/red]")
    else:
        misc.add_row("Current HP", f"[green]{pc.current_hp}[/green]")
    misc.add_row("AC", str(pc.ac))
    misc.add_row("Speed", str(pc.speed))
    misc.add_row("Proficiency Bonus", str(get_proficiency_bonus(pc.level)))
    misc.add_row("", "")

    columns.add_renderable(misc)

    # Ability Scores
    ability_scores = Table(expand=True, box=box.ROUNDED)
    ability_scores.add_column("Ability", justify="right")
    ability_scores.add_column("Score", justify="center", max_width=4)
    ability_scores.add_column("Modifier", justify="center", max_width=4)

    for ability, score in pc.ability_scores.items():
        ability_scores.add_row(
            ability.upper(), str(score), str(get_modifier(score))
        )

    columns.add_renderable(ability_scores)

    # Proficiencies
    proficiencies = Table(expand=True, box=box.ROUNDED)
    proficiencies.add_column("Prof", justify="center", max_width=2)
    proficiencies.add_column("Mod", justify="center", max_width=2)
    proficiencies.add_column("Skill", justify="right")
    proficiencies.add_column("Bonus", justify="center", max_width=5)

    for skill in list(Skill):

        value = get_modifier(pc.ability_scores[skill.mod_type])
        prof = ""
        if skill in pc.proficiencies["skills"]:
            prof = "‧"
            value += get_proficiency_bonus(pc.level)

        posneg = "+"
        if value < 0:
            posneg = "-"
        elif value == 0:
            posneg = ""
       
        proficiencies.add_row(
            prof,
            skill.mod_type.short_name,
            skill.name.capitalize(),
            f"{posneg}{value}",
        )

    columns.add_renderable(proficiencies)

    console.print(columns)


if __name__ == "__main__":
    import json
    from dmcli.character import PC

    console = Console()

    with open("data/grendor_herlsson.json", "r") as f:
        pc = PC.create_from_json(json.load(f))
    render_pc(pc, console)
