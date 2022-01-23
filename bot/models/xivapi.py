from typing import List, Optional
import unicodedata
from enum import Enum
import random

from pydantic import BaseModel, Field

class CharacterSearch(BaseModel):
    lodestone_id: int = Field(alias="ID")
    name: str = Field(alias="Name")
    server: str = Field(alias="Server")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Server is returned in format World (Data Center)
        # but the space is Latin1 non-breaking space
        # so we normalize to turn it back into a normal space
        # See https://stackoverflow.com/questions/10993612/how-to-remove-xa0-from-string-in-python
        self.server = unicodedata.normalize("NFKC", self.server)

    @property
    def world(self):
        return self.server.replace("(", "").replace(")", "").split(" ")[0]

    @property
    def data_center(self):
        return self.server.replace("(", "").replace(")", "").split(" ")[1]

class UnlockedState(BaseModel):
    job_id: Optional[int] = Field(alias="ID")
    job_name: str = Field(alias="Name")


class JobType(str, Enum):
    TANK = "Tank"
    DPS = "DPS"
    HEALER = "Healer"
    CRAFTER = "Crafter"
    GATHERER = "Gatherer"
    LIMITED = "Limited"


job_to_type = {
    "Gladiator": JobType.TANK,
    "Paladin": JobType.TANK,
    "Marauder": JobType.TANK,
    "Warrior": JobType.TANK,
    "Dark Knight": JobType.TANK,
    "Gunbreaker": JobType.TANK,
    "Conjurer": JobType.HEALER,
    "White Mage": JobType.HEALER,
    "Arcanist": JobType.DPS,
    "Scholar": JobType.HEALER,
    "Astrologian": JobType.HEALER,
    "Sage": JobType.HEALER,
    "Pugilist": JobType.DPS,
    "Monk": JobType.DPS,
    "Lancer": JobType.DPS,
    "Dragoon": JobType.DPS,
    "Rogue": JobType.DPS,
    "Ninja": JobType.DPS,
    "Samurai": JobType.DPS,
    "Reaper": JobType.DPS,
    "Archer": JobType.DPS,
    "Bard": JobType.DPS,
    "Machinist": JobType.DPS,
    "Dancer": JobType.DPS,
    "Thaumaturge": JobType.DPS,
    "Black Mage": JobType.DPS,
    "Summoner": JobType.DPS,
    "Red Mage": JobType.DPS,
    "Blue Mage (Limited Job)": JobType.LIMITED,
    "Carpenter": JobType.CRAFTER,
    "Blacksmith": JobType.CRAFTER,
    "Armorer": JobType.CRAFTER,
    "Goldsmith": JobType.CRAFTER,
    "Leatherworker": JobType.CRAFTER,
    "Weaver": JobType.CRAFTER,
    "Alchemist": JobType.CRAFTER,
    "Culinarian": JobType.CRAFTER,
    "Miner": JobType.GATHERER,
    "Botanist": JobType.GATHERER,
    "Fisher": JobType.GATHERER
}

job_to_short_name = {
    "Gladiator": "GLD",
    "Paladin": "PLD",
    "Marauder": "MRD",
    "Warrior": "WAR",
    "Dark Knight": "DRK",
    "Gunbreaker": "GNB",
    "Conjurer": "CNJ",
    "White Mage": "WHM",
    "Arcanist": "ACN",
    "Scholar": "SCH",
    "Astrologian": "AST",
    "Sage": "SGE",
    "Pugilist": "PGL",
    "Monk": "MNK",
    "Lancer": "LNC",
    "Dragoon": "DRG",
    "Rogue": "ROG",
    "Ninja": "NIN",
    "Samurai": "SAM",
    "Reaper": "RPR",
    "Archer": "ARC",
    "Bard": "BRD",
    "Machinist": "MCH",
    "Dancer": "DNC",
    "Thaumaturge": "THM",
    "Black Mage": "BLM",
    "Summoner": "SMN",
    "Red Mage": "RDM",
    "Blue Mage (Limited Job)": "BLU",
    "Carpenter": "CRP",
    "Blacksmith": "BSM",
    "Armorer": "ARM",
    "Goldsmith": "GSM",
    "Leatherworker": "LTW",
    "Weaver": "WVR",
    "Alchemist": "ALC",
    "Culinarian": "CUL",
    "Miner": "MIN",
    "Botanist": "BOT",
    "Fisher": "FSH"
}



class Job(BaseModel):
    level: int = Field(alias="Level")
    nested_data: UnlockedState = Field(alias="UnlockedState")

    @property
    def name(self) -> str:
        return self.nested_data.job_name

    @property
    def job_type(self) -> JobType:
        return job_to_type[self.name]

    @property
    def short_name(self) -> str:
        return job_to_short_name[self.name]


class Character(BaseModel):
    jobs: List[Job] = Field(alias="ClassJobs")
    data_center: str = Field(alias="DC")
    lodestone_id: int = Field(alias="ID")
    name: str = Field(alias="Name")
    server: str = Field(alias="Server")

    def _jobs_of_type(self, job_type: JobType) -> List[Job]:
        return [j for j in self.jobs if j.job_type == job_type]

    @property
    def tank_jobs(self) -> List[Job]:
        return self._jobs_of_type(JobType.TANK)

    @property
    def healer_jobs(self) -> List[Job]:
        return self._jobs_of_type(JobType.HEALER)

    @property
    def dps_jobs(self) -> List[Job]:
        return self._jobs_of_type(JobType.DPS)

    @property
    def crafting_jobs(self) -> List[Job]:
        return self._jobs_of_type(JobType.CRAFTER)

    @property
    def gathering_jobs(self) -> List[Job]:
        return self._jobs_of_type(JobType.GATHERER)

    def get_random_job(self, job_type: Optional[JobType] = None, min_level: Optional[int] = None, max_level: Optional[int] = None) -> Optional[Job]:
        matching_jobs = self._jobs_of_type(job_type) if job_type else self.jobs

        if min_level:
            matching_jobs = [j for j in matching_jobs if j.level >= min_level]

        if max_level:
            matching_jobs = [j for j in matching_jobs if j.level <= max_level]

        return random.choice(matching_jobs) if matching_jobs else None