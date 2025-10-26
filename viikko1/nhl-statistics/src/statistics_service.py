from enum import Enum
from player_reader import PlayerReader
from player import Player


class SortBy(Enum):
    POINTS = 1
    GOALS = 2
    ASSISTS = 3


class StatisticsService:
    def __init__(self, reader: PlayerReader):
        self._players = reader.get_players()

    def search(self, name: str):
        for player in self._players:
            if name in player.name:
                return player

        return None

    def team(self, team_name: str) -> list[Player]:
        players_of_team = filter(lambda player: player.team == team_name, self._players)

        return list(players_of_team)

    def top(self, how_many: int, sort_by: SortBy | None = None) -> list[Player]:
        def sort_by_key(player: Player):
            match sort_by:
                case SortBy.POINTS:
                    return player.points
                case SortBy.GOALS:
                    return player.goals
                case SortBy.ASSISTS:
                    return player.assists
                case _:
                    return player.points

        sorted_players = sorted(self._players, reverse=True, key=sort_by_key)

        result = []
        i = 0
        # This implementation seems a bit buggy:
        # - Why do we return top n plus one players?
        # - Why is there no bounds checking?
        while i <= how_many:
            result.append(sorted_players[i])
            i += 1

        return result
