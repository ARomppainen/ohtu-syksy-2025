from typing import Literal

_WIN_THRESHOLD = 4
_DEUCE_THRESHOLD = 3


class TennisGame:

    def __init__(self, player1_name: str, player2_name: str):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_points = 0
        self.player2_points = 0

    def won_point(self, player_name: str):
        if player_name == self.player1_name:
            self.player1_points += 1
        elif player_name == self.player2_name:
            self.player2_points += 1
        else:
            raise ValueError(f'Unknown player: "{player_name}"')

    def get_score(self):
        if self._is_even_game():
            return self._score_even_game()

        if self._is_advantage_or_won_game():
            return self._score_advantage_or_won_game()

        return self._score_other_cases()

    def _is_even_game(self) -> bool:
        return self.player1_points == self.player2_points

    def _score_even_game(self):
        if self.player1_points >= _DEUCE_THRESHOLD:
            return "Deuce"
        return f"{self._points_to_score(self.player1_points)}-All"

    def _is_advantage_or_won_game(self):
        return (
            self.player1_points >= _WIN_THRESHOLD
            or self.player2_points >= _WIN_THRESHOLD
        )

    def _score_advantage_or_won_game(self):
        points_difference = self.player1_points - self.player2_points

        if points_difference == 1:
            return self._score_advantage(1)
        if points_difference == -1:
            return self._score_advantage(2)
        if points_difference >= 2:
            return self._score_win(1)
        return self._score_win(2)

    @staticmethod
    def _score_advantage(player: Literal[1, 2]):
        return f"Advantage player{player}"

    @staticmethod
    def _score_win(player: Literal[1, 2]):
        return f"Win for player{player}"

    def _score_other_cases(self):
        score1 = self._points_to_score(self.player1_points)
        score2 = self._points_to_score(self.player2_points)
        return f"{score1}-{score2}"

    @staticmethod
    def _points_to_score(points: int):
        if points == 0:
            return "Love"
        if points == 1:
            return "Fifteen"
        if points == 2:
            return "Thirty"
        return "Forty"
