from copy import deepcopy
from datetime import datetime, timedelta
from typing import List, Optional

import requests
from cachetools import LRUCache, TTLCache, cached

from bot.constants import RELEVANT_WORLDS
from bot.models.xivapi import Character, CharacterSearch


class XIVAPIService:
    BASE_URL = "https://xivapi.com"

    def __init__(self, api_key: str):
        self._api_key = api_key

    def get(self, path: str, params: Optional[dict] = None) -> requests.Response:
        updated_params = deepcopy(params) if params else {}
        updated_params["private_key"] = self._api_key
        return requests.get(f"{self.BASE_URL}/{path}", params=updated_params)

    @cached(cache=LRUCache(maxsize=100))
    def character_id_from_name(self, name: str, worlds: List[str] = None) -> Optional[str]:
        """Retrieves basic information about a character
        (Lodestone ID and server) by name.
        """
        worlds = worlds or RELEVANT_WORLDS
        response = self.get("character/search", params={"name": name})
        characters = []
        for character in response.json()["Results"]:
            characters.append(CharacterSearch.parse_obj(character))

        try:
            return next(c for c in characters if c.world in worlds)
        except StopIteration:
            print(f"No character in the right datacenter/server for {name}")
            import pdb

            pdb.set_trace()
            return

    @cached(cache=TTLCache(maxsize=100, ttl=timedelta(hours=1), timer=datetime.now))
    def character_from_id(self, lodestone_id: int) -> Character:
        response = self.get(f"character/{lodestone_id}")
        return Character.parse_obj(response.json()["Character"])
