from copy import deepcopy
from typing import Optional

import requests

from bot.models.xivapi import Character, CharacterSearch


class XIVAPIService:
    BASE_URL = "https://xivapi.com"

    def __init__(self, api_key: str):
        self._api_key = api_key

    def get(self, path: str, params: Optional[dict] = None) -> requests.Response:
        updated_params = deepcopy(params) if params else {}
        updated_params["private_key"] = self._api_key
        return requests.get(f"{self.BASE_URL}/{path}", params=updated_params)

    def character_id_from_name(self, name: str) -> str:
        response = self.get("character/search", params={"name": name})
        characters = []
        for character in response.json()["Results"]:
            characters.append(CharacterSearch.parse_obj(character))

        # TODO: Take a data center argument so this filter isn't hardcoded
        return next(c for c in characters if c.data_center == "Crystal")

    def character_from_id(self, lodestone_id: int) -> Character:
        response = self.get(f"character/{lodestone_id}")
        return Character.parse_obj(response.json()["Character"])
