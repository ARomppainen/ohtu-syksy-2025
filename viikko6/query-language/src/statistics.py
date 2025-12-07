from matchers import Matcher
from player_reader import PlayerReader
from player import Player


def sort_by_points(player: Player):
    return player.points


class Statistics:
    def __init__(self, player_reader: PlayerReader):
        self._players = player_reader.get_players()

    def search(self, name):
        for player in self._players:
            if name in player.name:
                return player

        return None

    def team(self, team_name: str):
        players_of_team = filter(lambda player: player.team == team_name, self._players)

        return list(players_of_team)

    def top_scorers(self, how_many: int):
        sorted_players = sorted(self._players, reverse=True, key=sort_by_points)

        return sorted_players[:how_many]

    def matches(self, matcher: Matcher):
        matching_players = filter(matcher.test, self._players)

        return list(matching_players)
