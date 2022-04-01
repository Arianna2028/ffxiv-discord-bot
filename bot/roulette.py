import random
from typing import List, Optional

from bot.constants import MAX_LEVEL
from bot.models.roulette import Roulette, RouletteSelection, RouletteType
from bot.models.xivapi import Character

ALL_ROULETTES = [
    Roulette(
        name=RouletteType.EXPERT,
        label="Expert",
        num_tanks=1,
        num_healers=1,
        num_dps=2,
        min_job_level=MAX_LEVEL,
        gives_exp=False,
    ),
    Roulette(
        name=RouletteType.NORMAL_RAID,
        label="Normal Raids",
        num_tanks=2,
        num_healers=2,
        num_dps=4,
        min_job_level=60,
        aliases=["normal_raids", "normal-raid", "normal-raids"],
    ),
    Roulette(
        name=RouletteType.TRIAL,
        label="Trials",
        num_tanks=2,
        num_healers=2,
        num_dps=4,
        min_job_level=50,
        aliases=["trials"],
    ),
    Roulette(
        name=RouletteType.ALLIANCE_RAID,
        label="Alliance Raids",
        num_tanks=1,
        num_healers=2,
        num_dps=5,
        min_job_level=50,
        aliases=["alliance_raids", "alliance-raid", "alliance-raids"],
    ),
    Roulette(
        name=RouletteType.ZEROS,
        label="50/60/70/80s",
        num_tanks=1,
        num_healers=1,
        num_dps=2,
        min_job_level=50,
        aliases=["zero"],
    ),
    Roulette(
        name=RouletteType.LEVELING,
        label="Leveling",
        num_tanks=1,
        num_healers=1,
        num_dps=2,
        min_job_level=16,
    ),
]


def roulette_by_name(roulette_name: str) -> Optional[Roulette]:
    return next(
        (r for r in ALL_ROULETTES if r.name == roulette_name or roulette_name in r.aliases), None
    )


def random_by_role(roulette: Roulette, characters: List[Character]) -> List[RouletteSelection]:
    """Randomly selects a role for each character provided, given the constraints
    of a particular roulette.
    """

    selections: List[RouletteSelection] = []
    unselected_characters = random.sample(characters, len(characters))
    job_type_choices = random.sample(roulette.job_type_list, roulette.total_players)
    max_level = MAX_LEVEL - 1 if roulette.gives_exp else MAX_LEVEL
    for needed_job_type in job_type_choices:
        if not unselected_characters:
            break

        char = unselected_characters.pop()
        if job := char.get_random_job(
            needed_job_type, min_level=roulette.min_job_level, max_level=max_level
        ):
            selections.append(RouletteSelection(job=job, character=char))
        else:
            # Put the unmatched person back at the front of the list
            # to be matched for the next job type
            unselected_characters = [char] + unselected_characters

    return selections


def shuffled_roulettes() -> List[Roulette]:
    return random.sample(ALL_ROULETTES, len(ALL_ROULETTES))
