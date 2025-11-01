import logging
from typing import List
import requests
from player import Player

HTTP_OK = 200


class PlayerReader:
    def __init__(self, url: str):
        self._url = url
        self._logger = logging.getLogger(__name__)

    def get_players(self) -> List[Player]:
        response = requests.get(self._url, timeout=10)
        if response.status_code == HTTP_OK:
            return [Player(**row) for row in response.json()]
        self._logger.error(
            "Could not get list of players, status: %s, content: %s",
            response.status_code,
            str(response.content),
        )
        raise RuntimeError("Unexpected HTTP status code")
