from itertools import zip_longest
from typing import TYPE_CHECKING

from rich import box
from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from dmcli.special_types import Skill
from dmcli.utils import get_modifier, get_proficiency_bonus, halved

if TYPE_CHECKING:
    from dmcli.character import PC


def render_pc(pc: "PC", console: Console):
    console.print(
        Panel(f"[bold green]{pc.name}[/bold green]"), justify="center"
    )
    columns = Columns(expand=True, padding=0)

    # Basic Info
    basic_info = Table(expand=True, box=box.ROUNDED, title="Character Details")
    basic_info.add_column("Field", justify="right")
    basic_info.add_column("Value")

    basic_info.add_row("Nickname", pc.nickname)
    basic_info.add_row("Race", pc.race.capitalize())
    basic_info.add_row("Class", pc.dnd_class.capitalize())
    basic_info.add_row("Level", str(pc.level))
    basic_info.add_row("Gender", pc.gender.capitalize())
    basic_info.add_row("", "")

    # Misc Stats
    misc = Table(expand=True, box=box.ROUNDED, title="More Details")
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

    # Ability Scores
    ability_scores = Table(
        expand=True, box=box.ROUNDED, title="Ability Scores"
    )
    ability_scores.add_column("Ability", justify="right")
    ability_scores.add_column("Score", justify="center", max_width=4)
    ability_scores.add_column("Modifier", justify="center", max_width=4)

    for ability, score in pc.ability_scores.items():
        ability_scores.add_row(
            ability.upper(), str(score), str(get_modifier(score))
        )

    # Skills
    skills = Table(expand=True, box=box.ROUNDED, title="Skills")
    skills.add_column("Prof", justify="center", max_width=2)
    skills.add_column("Mod", justify="center", max_width=2)
    skills.add_column("Skill", justify="right")
    skills.add_column("Bonus", justify="center", max_width=5)

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
            posneg = " "

        skills.add_row(
            prof,
            skill.mod_type.short_name,
            skill.name.capitalize(),
            f"{posneg}{value}",
        )

    # Passives
    passives = Table(expand=True, box=box.ROUNDED, title="Passives")
    passives.add_column("Perception", justify="center")
    passives.add_column("Investigation", justify="center")
    passives.add_column("Insight", justify="center")

    passive_row_vals = []
    for score in [Skill.PERCEPTION, Skill.INVESTIGATION, Skill.INSIGHT]:
        value = get_modifier(pc.ability_scores[score.mod_type]) + 10
        if score in pc.proficiencies["skills"]:
            value += get_proficiency_bonus(pc.level)
        passive_row_vals.append(str(value))

    passives.add_row(*passive_row_vals)

    # Proficiencies
    proficiencies = Table(expand=True, box=box.ROUNDED, title="Proficiencies")
    relevant_proficiencies = ["weapons", "armor", "tools"]
    pd = [pc.languages] + [pc.proficiencies[k] for k in relevant_proficiencies]

    proficiencies.add_column("Languages", justify="right")
    for rp in relevant_proficiencies:
        proficiencies.add_column(rp.capitalize(), justify="right")

    for profs in zip_longest(*pd, fillvalue=""):
        proficiencies.add_row(*profs)

    columns.add_renderable(basic_info)
    columns.add_renderable(misc)
    columns.add_renderable(ability_scores)
    columns.add_renderable(passives)
    columns.add_renderable(proficiencies)
    columns.add_renderable(skills)
    console.print(columns)


if __name__ == "__main__":
    import json

    from dmcli.character import PC

    console = Console()

    with open("data/grendor_herlsson.json", "r") as f:
        pc = PC.create_from_json(json.load(f))
    render_pc(pc, console)
