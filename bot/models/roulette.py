from enum import Enum
from functools import cached_property
from typing import List

from pydantic import BaseModel

from .xivapi import Character, Job, JobType


class RouletteType(str, Enum):
    LEVELING = "leveling"
    EXPERT = "expert"
    ALLIANCE_RAID = "alliance_raid"
    NORMAL_RAID = "normal_raid"
    TRIAL = "trial"
    ZEROS = "zeros"  # 50s/60s/70s/80s


class Roulette(BaseModel):
    class Config:
        keep_untouched = (cached_property,)

    name: RouletteType
    aliases: List[str] = []
    label: str
    num_tanks: int
    num_healers: int
    num_dps: int
    min_job_level: int
    gives_exp: bool = True

    @cached_property
    def total_players(self) -> int:
        return self.num_tanks + self.num_healers + self.num_dps

    @cached_property
    def job_type_list(self) -> List[JobType]:
        tanks = [JobType.TANK] * self.num_tanks
        healers = [JobType.HEALER] * self.num_healers
        dps = [JobType.DPS] * self.num_dps
        return tanks + healers + dps


class RouletteSelection(BaseModel):
    """Represents a selected job for a character to play
    in a specific roulette.
    """

    job: Job
    character: Character

    def __repr__(self) -> str:
        return f"{self.character.name}: {self.job.name}"
