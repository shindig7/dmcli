import random
import re

import rich

system_random = random.SystemRandom()


def roll(dice_combo: list[str]) -> None:
    dice_combo = dice_combo[0]
    if dice_combo == "":
        roll("1d20")
    else:
        if "+" in dice_combo:
            dice, bonus = dice_combo.split("+")
            bonus = int(bonus)
        elif "-" in dice_combo:
            dice, bonus = dice_combo.split("-")
            bonus = int(bonus) * -1
        else:
            dice, bonus = dice_combo, 0

        dice_count, dice_sides = re.split("[dD]", dice)
        if dice_count == "":
            dice_count = 1

        rolls = []
        for i in range(int(dice_count)):
            rolls.append(system_random.randint(1, int(dice_sides)))

        rich.print(sum(rolls) + bonus, str(rolls))
        return sum(rolls) + bonus


if __name__ == "__main__":
    rich.print(roll("1d20"))
    rich.print(roll("2d8"))
    rich.print(roll("10d100"))
