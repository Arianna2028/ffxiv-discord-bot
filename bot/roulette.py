from typing import List
from bot.models.roulette import Roulette, RouletteSelection
from bot.models.xivapi import Character, JobType
import random
from bot.constants import MAX_LEVEL


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
        if job := char.get_random_job(needed_job_type, min_level=roulette.min_job_level, max_level=max_level):
            selections.append(RouletteSelection(job=job, character=char))
        else:
            # Put the unmatched person back at the front of the list
            # to be matched for the next job type
            unselected_characters = [char] + unselected_characters

    return selections