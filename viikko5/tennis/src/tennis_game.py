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

        score = ""
        temp_score = 0

        for i in range(1, 3):
            if i == 1:
                temp_score = self.m_score1
            else:
                score = score + "-"
                temp_score = self.m_score2

            if temp_score == 0:
                score = score + "Love"
            elif temp_score == 1:
                score = score + "Fifteen"
            elif temp_score == 2:
                score = score + "Thirty"
            elif temp_score == 3:
                score = score + "Forty"

        return score

    def _is_even_game(self) -> bool:
        return self.m_score1 == self.m_score2

    def _score_even_game(self):
        if self.m_score1 == 0:
            return "Love-All"
        if self.m_score1 == 1:
            return "Fifteen-All"
        if self.m_score2 == 2:
            return "Thirty-All"
        return "Deuce"

    def _is_advantage_or_won_game(self):
        return self.m_score1 >= 4 or self.m_score2 >= 4

    def _score_advantage_or_won_game(self):
        difference = self.m_score1 - self.m_score2

        if difference == 1:
            return "Advantage player1"
        if difference == -1:
            return "Advantage player2"
        if difference >= 2:
            return "Win for player1"
        return "Win for player2"
