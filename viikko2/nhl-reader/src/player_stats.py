from typing import List
from player import Player
from player_reader import PlayerReader

class PlayerStats:
    def __init__(self, reader: PlayerReader):
        self._data = reader.get_players()
    
    def top_scorers_by_nationality(self, nationality: str) -> List[Player]:
        filtered = filter(lambda p: p.nationality == nationality, self._data)
        return sorted(filtered, key=lambda p: p.score, reverse=True)
