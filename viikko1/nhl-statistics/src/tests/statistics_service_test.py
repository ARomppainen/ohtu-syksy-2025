from parameterized import parameterized
import unittest
from player import Player
from statistics_service import SortBy, StatisticsService


class PlayerReaderStub:
    def __init__(self, data: list[Player]):
        self._data = data

    def get_players(self) -> list[Player]:
        return self._data


class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        self.service = StatisticsService(
            PlayerReaderStub(
                [
                    Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
                    Player("Lemieux", "PIT", 45, 54),  # 45+54 = 99
                    Player("Kurri", "EDM", 37, 53),  # 37+53 = 90
                    Player("Yzerman", "DET", 42, 56),  # 42+56 = 98
                    Player("Gretzky", "EDM", 35, 89),  # 35+89 = 124
                ]
            )
        )

    @parameterized.expand(
        [
            ("Semenko", 16),
            ("Kurri", 90),
            ("Gretzky", 124),
        ]
    )
    def test_search_should_return_player_by_name(self, name: str, points: int):
        result = self.service.search(name)
        self.assertEqual(result.name, name)
        self.assertEqual(result.points, points)

    def test_search_should_return_none_if_player_not_found(self):
        result = self.service.search("foobar")
        self.assertIsNone(result)

    @parameterized.expand(
        [
            ("EDM", ["Semenko", "Kurri", "Gretzky"]),
            ("PIT", ["Lemieux"]),
            ("DET", ["Yzerman"]),
            ("foobar", []),
        ]
    )
    def test_team_should_return_list_of_players_in_that_team(
        self, team_name: str, expected: list[str]
    ):
        result = self.service.team(team_name)
        self.assertEqual(len(result), len(expected))
        for i, player in enumerate(result):
            self.assertEqual(player.name, expected[i])

    @parameterized.expand(
        [
            (0, None, ["Gretzky"]),
            (3, None, ["Gretzky", "Lemieux", "Yzerman", "Kurri"]),
            (3, SortBy.POINTS, ["Gretzky", "Lemieux", "Yzerman", "Kurri"]),
            (1, SortBy.GOALS, ["Lemieux", "Yzerman"]),
            (2, SortBy.ASSISTS, ["Gretzky", "Yzerman", "Lemieux"]),
        ]
    )
    def test_top_should_return_top_n_plus_one_players(
        self, n: int, sort_by: SortBy | None, expected: list[str]
    ):
        result = self.service.top(n, sort_by)
        self.assertEqual(len(result), n + 1)
        for i, player in enumerate(result):
            self.assertEqual(player.name, expected[i])

    def test_top_should_return_empty_list_if_value_is_negative(self):
        result = self.service.top(-1)
        self.assertEqual(result, [])
