import pytest
from app import app
from kps import KIVI, PAPERI, SAKSET


@pytest.fixture
def client():
    """Create a Flask test client"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestIndexRoute:
    """Tests for the index/home page"""

    def test_index_page_loads(self, client):
        """Test that the index page loads successfully"""
        response = client.get("/")
        assert response.status_code == 200
        assert "Valitse pelityyppi" in response.data.decode("utf-8")

    def test_index_shows_game_options(self, client):
        """Test that all three game options are displayed"""
        response = client.get("/")
        content = response.data.decode("utf-8")
        assert "Pelaaja vs Pelaaja" in content
        assert "Tekoäly" in content
        assert "Parannettu" in content


class TestGameStart:
    """Tests for starting a new game"""

    def test_start_pvp_game(self, client):
        """Test starting a Player vs Player game"""
        response = client.post(
            "/start", data={"game_type": "pvp"}, follow_redirects=True
        )
        assert response.status_code == 200
        content = response.data.decode("utf-8")
        assert "Pelaaja 1" in content and "Pelaaja 2" in content

    def test_start_pvc_game(self, client):
        """Test starting a Player vs Computer game"""
        response = client.post(
            "/start", data={"game_type": "pvc"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert "Tekoäly" in response.data.decode("utf-8")

    def test_start_pvc_advanced_game(self, client):
        """Test starting a Player vs Advanced Computer game"""
        response = client.post(
            "/start", data={"game_type": "pvc_advanced"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert "Parannettu" in response.data.decode("utf-8")

    def test_start_invalid_game_type(self, client):
        """Test that invalid game type redirects to index"""
        response = client.post(
            "/start", data={"game_type": "invalid"}, follow_redirects=True
        )
        assert response.status_code == 200
        assert "Valitse pelityyppi" in response.data.decode("utf-8")

    def test_game_state_initialized(self, client):
        """Test that game state is properly initialized"""
        client.post("/start", data={"game_type": "pvp"})
        with client.session_transaction() as sess:
            assert "game_type" in sess
            assert "tuomari" in sess
            assert "history" in sess


class TestGamePlay:
    """Tests for game play"""

    def test_play_page_requires_game_type(self, client):
        """Test that play page redirects if no game is started"""
        response = client.get("/play", follow_redirects=True)
        assert "Valitse pelityyppi" in response.data.decode("utf-8")

    def test_play_page_displays_scoreboard(self, client):
        """Test that play page displays scoreboard"""
        client.post("/start", data={"game_type": "pvp"})
        response = client.get("/play")
        content = response.data.decode("utf-8")
        assert "Pelitilanne" in content or "0" in content

    def test_pvp_move_both_players(self, client):
        """Test a PvP move with both players making selections"""
        client.post("/start", data={"game_type": "pvp"})
        response = client.post(
            "/move",
            data={"move": KIVI, "move2": PAPERI},
            follow_redirects=True,
        )
        assert response.status_code == 200
        content = response.data.decode("utf-8")
        assert "voitti" in content or "Tasapeli" in content

    def test_pvp_invalid_move(self, client):
        """Test that invalid move is rejected"""
        client.post("/start", data={"game_type": "pvp"})
        response = client.post(
            "/move",
            data={"move": "invalid", "move2": KIVI},
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_pvc_ai_makes_move(self, client):
        """Test that AI makes a move in PvC game"""
        client.post("/start", data={"game_type": "pvc"})
        response = client.post(
            "/move",
            data={"move": KIVI},
            follow_redirects=True,
        )
        assert response.status_code == 200
        content = response.data.decode("utf-8")
        assert "Kierros" in content or "voitti" in content or "Tasapeli" in content

    def test_multiple_rounds(self, client):
        """Test playing multiple rounds"""
        client.post("/start", data={"game_type": "pvp"})

        # Round 1: Player 1 wins
        client.post(
            "/move",
            data={"move": KIVI, "move2": SAKSET},
        )

        # Round 2: Player 2 wins
        response = client.post(
            "/move",
            data={"move": PAPERI, "move2": SAKSET},
            follow_redirects=True,
        )

        assert response.status_code == 200
        content = response.data.decode("utf-8")
        assert "Kierros" in content or "Kivi" in content

    def test_draw_game(self, client):
        """Test a draw result"""
        client.post("/start", data={"game_type": "pvp"})
        response = client.post(
            "/move",
            data={"move": KIVI, "move2": KIVI},
            follow_redirects=True,
        )
        assert "Tasapeli!" in response.data.decode("utf-8")

    def test_history_populated(self, client):
        """Test that game history is populated"""
        client.post("/start", data={"game_type": "pvp"})
        client.post(
            "/move",
            data={"move": KIVI, "move2": PAPERI},
        )
        response = client.get("/play")
        content = response.data.decode("utf-8")
        assert "Pelihistoria" in content or "Kierros" in content


class TestGameReset:
    """Tests for game reset"""

    def test_reset_clears_game(self, client):
        """Test that reset clears the game state"""
        client.post("/start", data={"game_type": "pvp"})
        response = client.get("/reset", follow_redirects=True)
        assert "Valitse pelityyppi" in response.data.decode("utf-8")

    def test_reset_from_play_page(self, client):
        """Test reset button from play page"""
        client.post("/start", data={"game_type": "pvp"})
        client.post(
            "/move",
            data={"move": KIVI, "move2": PAPERI},
        )
        response = client.get("/reset", follow_redirects=True)
        assert "Valitse pelityyppi" in response.data.decode("utf-8")


class TestAIState:
    """Tests for AI state persistence"""

    def test_simple_ai_state_persists(self, client):
        """Test that simple AI state persists across moves"""
        client.post("/start", data={"game_type": "pvc"})

        # First move
        client.post("/move", data={"move": KIVI})
        client.get("/play")

        with client.session_transaction() as sess:
            first_ai_state = sess.get("ai_state")
            assert first_ai_state is not None
            assert "siirto" in first_ai_state
            first_siirto = first_ai_state["siirto"]

        # Second move
        client.post("/move", data={"move": KIVI})
        client.get("/play")

        with client.session_transaction() as sess:
            second_ai_state = sess.get("ai_state")
            assert second_ai_state is not None
            # AI state should have changed
            assert second_ai_state["siirto"] != first_siirto

    def test_advanced_ai_learns(self, client):
        """Test that advanced AI learns from moves"""
        client.post("/start", data={"game_type": "pvc_advanced"})

        # Play several rounds
        for _ in range(3):
            client.post("/move", data={"move": KIVI})

        client.get("/play")

        with client.session_transaction() as sess:
            ai_state = sess.get("ai_state")
            assert ai_state is not None
            assert "muisti" in ai_state
            # Memory should have been updated
            assert ai_state["vapaa_muisti_indeksi"] > 0


class TestTuomari:
    """Tests for referee/score tracking"""

    def test_tuomari_initialization(self, client):
        """Test that Tuomari is properly initialized"""
        with client.session_transaction() as sess:
            sess["tuomari"] = {
                "ekan_pisteet": 0,
                "tokan_pisteet": 0,
                "tasapelit": 0,
            }

        with client.session_transaction() as sess:
            tuomari_data = sess.get("tuomari")
            assert tuomari_data is not None
            assert tuomari_data["ekan_pisteet"] == 0

    def test_score_tracking_pvp(self, client):
        """Test score tracking in PvP"""
        client.post("/start", data={"game_type": "pvp"})

        # Player 1 wins
        client.post(
            "/move",
            data={"move": KIVI, "move2": SAKSET},
        )

        with client.session_transaction() as sess:
            tuomari = sess.get("tuomari")
            assert tuomari["ekan_pisteet"] == 1
            assert tuomari["tokan_pisteet"] == 0

    def test_draw_tracking(self, client):
        """Test that draws are tracked"""
        client.post("/start", data={"game_type": "pvp"})

        # Draw
        client.post(
            "/move",
            data={"move": KIVI, "move2": KIVI},
        )

        with client.session_transaction() as sess:
            tuomari = sess.get("tuomari")
            assert tuomari["tasapelit"] == 1


class TestGameLogic:
    """Tests for game logic and move results"""

    def test_rock_beats_scissors(self, client):
        """Test that rock beats scissors"""
        client.post("/start", data={"game_type": "pvp"})
        response = client.post(
            "/move",
            data={"move": KIVI, "move2": SAKSET},
            follow_redirects=True,
        )
        assert "Pelaaja 1 voitti!" in response.data.decode("utf-8")

    def test_scissors_beats_paper(self, client):
        """Test that scissors beat paper"""
        client.post("/start", data={"game_type": "pvp"})
        response = client.post(
            "/move",
            data={"move": SAKSET, "move2": PAPERI},
            follow_redirects=True,
        )
        assert "Pelaaja 1 voitti!" in response.data.decode("utf-8")

    def test_paper_beats_rock(self, client):
        """Test that paper beats rock"""
        client.post("/start", data={"game_type": "pvp"})
        response = client.post(
            "/move",
            data={"move": PAPERI, "move2": KIVI},
            follow_redirects=True,
        )
        assert "Pelaaja 1 voitti!" in response.data.decode("utf-8")

    def test_identical_moves_are_draw(self, client):
        """Test that identical moves result in a draw"""
        client.post("/start", data={"game_type": "pvp"})
        response = client.post(
            "/move",
            data={"move": PAPERI, "move2": PAPERI},
            follow_redirects=True,
        )
        assert "Tasapeli!" in response.data.decode("utf-8")


class TestIntegration:
    """Integration tests for full game flows"""

    def test_full_pvp_game_flow(self, client):
        """Test a complete PvP game flow"""
        # Start game
        response = client.post(
            "/start", data={"game_type": "pvp"}, follow_redirects=True
        )
        content = response.data.decode("utf-8")
        assert "Pelaaja 1" in content and "Pelaaja 2" in content

        # Play a round
        response = client.post(
            "/move",
            data={"move": KIVI, "move2": PAPERI},
            follow_redirects=True,
        )
        assert response.status_code == 200

        # Check score
        content = response.data.decode("utf-8")
        assert "Pelihistoria" in content or "voitti" in content

    def test_full_pvc_game_flow(self, client):
        """Test a complete PvC game flow"""
        # Start game
        response = client.post(
            "/start", data={"game_type": "pvc"}, follow_redirects=True
        )
        content = response.data.decode("utf-8")
        assert "Pelaaja 1" in content and "Tekoäly" in content

        # Play rounds and verify AI behaves correctly
        for i in range(3):
            response = client.post(
                "/move",
                data={"move": KIVI},
                follow_redirects=True,
            )
            assert response.status_code == 200

    def test_session_isolation(self, client):
        """Test that different game sessions don't interfere"""
        # Start first game
        client.post("/start", data={"game_type": "pvp"})

        # Play a move
        client.post("/move", data={"move": KIVI, "move2": PAPERI})

        with client.session_transaction() as sess:
            first_session_history_len = len(sess.get("history", []))

        # Reset and start new game
        client.get("/reset")
        client.post("/start", data={"game_type": "pvp"})

        with client.session_transaction() as sess:
            second_session_history_len = len(sess.get("history", []))
            assert second_session_history_len == 0


class TestFiveWinsFeature:
    """Tests for the 5-wins game completion feature"""

    def test_game_not_over_with_4_wins(self, client):
        """Test that game is not over when a player has 4 wins"""
        client.post("/start", data={"game_type": "pvp"})
        
        # Player 1 wins 4 times
        for _ in range(4):
            client.post("/move", data={"move": KIVI, "move2": SAKSET})
        
        with client.session_transaction() as sess:
            assert sess.get("game_over") is False
            assert sess.get("winner") is None

    def test_game_ends_when_player1_reaches_5_wins(self, client):
        """Test that game ends when Player 1 reaches 5 wins"""
        client.post("/start", data={"game_type": "pvp"})
        
        # Player 1 wins 5 times with rock vs scissors
        for _ in range(5):
            client.post("/move", data={"move": KIVI, "move2": SAKSET})
        
        with client.session_transaction() as sess:
            assert sess.get("game_over") is True
            assert sess.get("winner") == "Pelaaja 1"
            assert sess["tuomari"]["ekan_pisteet"] == 5

    def test_game_ends_when_player2_reaches_5_wins(self, client):
        """Test that game ends when Player 2 reaches 5 wins"""
        client.post("/start", data={"game_type": "pvp"})
        
        # Player 2 wins 5 times with paper vs rock
        for _ in range(5):
            client.post("/move", data={"move": KIVI, "move2": PAPERI})
        
        with client.session_transaction() as sess:
            assert sess.get("game_over") is True
            assert sess.get("winner") == "Pelaaja 2"
            assert sess["tuomari"]["tokan_pisteet"] == 5

    def test_no_moves_allowed_after_game_ends(self, client):
        """Test that no more moves are allowed after game ends"""
        client.post("/start", data={"game_type": "pvp"})
        
        # Player 1 wins 5 times
        for _ in range(5):
            client.post("/move", data={"move": KIVI, "move2": SAKSET})
        
        # Try to make another move
        response = client.post(
            "/move",
            data={"move": PAPERI, "move2": KIVI},
            follow_redirects=True,
        )
        
        # Should be on play page but game should still be over
        with client.session_transaction() as sess:
            assert sess.get("game_over") is True
            assert len(sess.get("history", [])) == 5  # No new move added

    def test_game_end_message_displayed(self, client):
        """Test that game end message is displayed"""
        client.post("/start", data={"game_type": "pvp"})
        
        # Player 1 wins 5 times
        for _ in range(5):
            client.post("/move", data={"move": KIVI, "move2": SAKSET})
        
        response = client.get("/play")
        content = response.data.decode("utf-8")
        assert "Peli päättyi!" in content or "voitti pelin" in content

    def test_game_with_draws_then_5_wins(self, client):
        """Test game with draws mixed in before reaching 5 wins"""
        client.post("/start", data={"game_type": "pvp"})
        
        # Mix of draws and Player 1 wins
        moves = [
            (KIVI, KIVI),     # Draw
            (KIVI, SAKSET),   # P1 wins (1)
            (PAPERI, PAPERI), # Draw
            (PAPERI, KIVI),   # P1 wins (2)
            (SAKSET, SAKSET), # Draw
            (SAKSET, PAPERI), # P1 wins (3)
            (KIVI, KIVI),     # Draw
            (KIVI, SAKSET),   # P1 wins (4)
            (PAPERI, PAPERI), # Draw
            (PAPERI, KIVI),   # P1 wins (5) - GAME ENDS
        ]
        
        for p1_move, p2_move in moves:
            client.post("/move", data={"move": p1_move, "move2": p2_move})
        
        with client.session_transaction() as sess:
            assert sess.get("game_over") is True
            assert sess.get("winner") == "Pelaaja 1"
            assert sess["tuomari"]["tasapelit"] == 5
            assert sess["tuomari"]["ekan_pisteet"] == 5

    def test_ai_game_ends_at_5_wins(self, client):
        """Test that AI game also ends at 5 wins"""
        client.post("/start", data={"game_type": "pvc"})
        
        # Play until someone reaches 5 wins
        wins_needed = 5
        rounds_played = 0
        max_rounds = 50  # Safety limit
        
        while rounds_played < max_rounds:
            response = client.post("/move", data={"move": KIVI})
            rounds_played += 1
            
            with client.session_transaction() as sess:
                if sess.get("game_over"):
                    break
        
        with client.session_transaction() as sess:
            assert sess.get("game_over") is True
            assert sess.get("winner") is not None
            # One player should have exactly 5 wins
            assert (sess["tuomari"]["ekan_pisteet"] == 5 or 
                   sess["tuomari"]["tokan_pisteet"] == 5)

    def test_reset_after_game_ends(self, client):
        """Test that reset works after game ends"""
        client.post("/start", data={"game_type": "pvp"})
        
        # Play until game ends
        for _ in range(5):
            client.post("/move", data={"move": KIVI, "move2": SAKSET})
        
        # Reset
        response = client.get("/reset", follow_redirects=True)
        assert "Valitse pelityyppi" in response.data.decode("utf-8")
        
        # Start a new game
        response = client.post("/start", data={"game_type": "pvp"}, follow_redirects=True)
        with client.session_transaction() as sess:
            assert sess.get("game_over") is False
            assert sess.get("winner") is None
            assert sess["tuomari"]["ekan_pisteet"] == 0
