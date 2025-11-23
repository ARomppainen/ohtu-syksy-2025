from typing import Literal

_WIN_THRESHOLD = 4
_DEUCE_THRESHOLD = 3


class TennisGame:

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_score1 = 0
        self.m_score2 = 0

    def won_point(self, player_name):
        if player_name == "player1":
            self.m_score1 = self.m_score1 + 1
        else:
            self.m_score2 = self.m_score2 + 1

    def get_score(self):
        if self._is_even_game():
            return self._score_even_game()

        if self._is_advantage_or_won_game():
            return self._score_advantage_or_won_game()

        return self._score_other_cases()

    def _is_even_game(self) -> bool:
        return self.m_score1 == self.m_score2

    def _score_even_game(self):
        if self.m_score1 >= _DEUCE_THRESHOLD:
            return "Deuce"
        return f"{self._points_to_score(self.m_score1)}-All"

    def _is_advantage_or_won_game(self):
        return self.m_score1 >= _WIN_THRESHOLD or self.m_score2 >= _WIN_THRESHOLD

    def _score_advantage_or_won_game(self):
        difference = self.m_score1 - self.m_score2

        if difference == 1:
            return self._score_advantage(1)
        if difference == -1:
            return self._score_advantage(2)
        if difference >= 2:
            return self._score_win(1)
        return self._score_win(2)

    @staticmethod
    def _score_advantage(player: Literal[1, 2]):
        return f"Advantage player{player}"

    @staticmethod
    def _score_win(player: Literal[1, 2]):
        return f"Win for player{player}"

    def _score_other_cases(self):
        score1 = self._points_to_score(self.m_score1)
        score2 = self._points_to_score(self.m_score2)
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
