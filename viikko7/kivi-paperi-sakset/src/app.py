from flask import Flask, render_template, request, session, redirect, url_for
import secrets
from kps_factory import Pelityyppi, luo_kps_peli
from tuomari import Tuomari
from kps import KIVI, PAPERI, SAKSET

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)


def get_game():
    """Retrieve the current game from the session"""
    if 'game_type' not in session:
        return None
    
    game_type = Pelityyppi(session['game_type'])
    
    # Create a custom input/print function for web interface
    def web_input(prompt):
        return session.get('last_move', '')
    
    def web_print(msg):
        pass  # We'll handle printing differently
    
    game = luo_kps_peli(game_type)
    game._input = web_input
    game._print = web_print
    
    return game


def get_tuomari():
    """Get or create a Tuomari (referee) for the current game"""
    if 'tuomari' not in session:
        session['tuomari'] = {
            'ekan_pisteet': 0,
            'tokan_pisteet': 0,
            'tasapelit': 0
        }
    
    tuomari = Tuomari()
    tuomari.ekan_pisteet = session['tuomari']['ekan_pisteet']
    tuomari.tokan_pisteet = session['tuomari']['tokan_pisteet']
    tuomari.tasapelit = session['tuomari']['tasapelit']
    
    return tuomari


def save_tuomari(tuomari):
    """Save the Tuomari state to session"""
    session['tuomari'] = {
        'ekan_pisteet': tuomari.ekan_pisteet,
        'tokan_pisteet': tuomari.tokan_pisteet,
        'tasapelit': tuomari.tasapelit
    }


@app.route('/')
def index():
    """Main page - game selection"""
    session.clear()
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start_game():
    """Start a new game with the selected game type"""
    game_type = request.form.get('game_type')
    
    if game_type == 'pvp':
        session['game_type'] = Pelityyppi.PELAAJA_VS_PELAAJA.value
    elif game_type == 'pvc':
        session['game_type'] = Pelityyppi.PELAAJA_VS_TEKOALY.value
    elif game_type == 'pvc_advanced':
        session['game_type'] = Pelityyppi.PELAAJA_VS_PAREMPI_TEKOALY.value
    else:
        return redirect(url_for('index'))
    
    session['tuomari'] = {
        'ekan_pisteet': 0,
        'tokan_pisteet': 0,
        'tasapelit': 0
    }
    session['history'] = []
    
    return redirect(url_for('play'))


@app.route('/play')
def play():
    """Game play page"""
    if 'game_type' not in session:
        return redirect(url_for('index'))
    
    tuomari = get_tuomari()
    game_type = Pelityyppi(session['game_type'])
    history = session.get('history', [])
    
    # Determine opponent name
    if game_type == Pelityyppi.PELAAJA_VS_PELAAJA:
        opponent = "Pelaaja 2"
    elif game_type == Pelityyppi.PELAAJA_VS_TEKOALY:
        opponent = "Tekoäly"
    else:
        opponent = "Parannettu Tekoäly"
    
    return render_template('play.html', 
                         tuomari=tuomari, 
                         opponent=opponent,
                         history=history)


@app.route('/move', methods=['POST'])
def make_move():
    """Process a move from player 1"""
    if 'game_type' not in session:
        return redirect(url_for('index'))
    
    player1_move = request.form.get('move')
    
    # Validate move
    if player1_move not in [KIVI, PAPERI, SAKSET]:
        return redirect(url_for('play'))
    
    # Get the game and determine player 2's move
    game = get_game()
    game_type = Pelityyppi(session['game_type'])
    
    if game_type == Pelityyppi.PELAAJA_VS_PELAAJA:
        # For PvP, player 2 move comes from the form
        player2_move = request.form.get('move2')
        if player2_move not in [KIVI, PAPERI, SAKSET]:
            return redirect(url_for('play'))
    else:
        # For AI games, get AI's move
        session['last_move'] = player1_move
        player2_move = game._toisen_siirto(player1_move)
    
    # Update referee
    tuomari = get_tuomari()
    tuomari.kirjaa_siirto(player1_move, player2_move)
    save_tuomari(tuomari)
    
    # Save to history
    history = session.get('history', [])
    
    # Determine result
    if player1_move == player2_move:
        result = "Tasapeli!"
    elif ((player1_move == KIVI and player2_move == SAKSET) or
          (player1_move == SAKSET and player2_move == PAPERI) or
          (player1_move == PAPERI and player2_move == KIVI)):
        result = "Pelaaja 1 voitti!"
    else:
        result = "Pelaaja 2 voitti!"
    
    # Convert moves to readable format
    move_names = {KIVI: "Kivi", PAPERI: "Paperi", SAKSET: "Sakset"}
    history.append({
        'round': len(history) + 1,
        'player1': move_names[player1_move],
        'player2': move_names[player2_move],
        'result': result
    })
    session['history'] = history
    
    return redirect(url_for('play'))


@app.route('/reset')
def reset():
    """Reset the game"""
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
