# Kivi, paperi ja sakset web-käyttöliittymän rakentaminen AI-avusteisesti

Useamman promptin jälkeen, lopputuloksena oli enimmäkseen toimiva sovellus.
Varmistin toimivuuden manuaalitestauksella, mutta en voi taata, että sovellus
toimisi täysin loogisesti oikein.

Annoin agentille yhteensä kymmenen syötettä. Jouduin hylkäämään näistä kahden
tuotoksen, koska agentti ei onnistunut bugikorjauksessa (korjasin bugin käsin).

Agentti generoi kaiken Python-koodin moduuleihin app.py ja app_test.py.
Olemassaolevia moduuleja agentti ei muokannut lainkaan. Tämän lisäksi agentti
käytti JavaScriptiä play.html templatessa. Alkuperäistä koodia agentti ei
muokannut lainkaan.

Generoitua koodia on melko paljon ja se on laadullisesti heikkoa. Metodit ovat
pitkiä, taikasanoja käytetään jatkuvasti, privaattimuuttujia muokataan joka
paikassa ja koko sovelluslogiikka on rakennettu web-rajapintakerrokseen.
Generoiduista testeistä on vaikea sanoa, testaavatko ne oikeita asioita. Testien
nimet ja jaottelu näyttävät yllättävän hyviltä.

Opin tästä ainakin sen, että agentit eivät näytä refaktoroivan olemassaolevaa
koodia, ellei niitä selvästi komenneta siihen. En myöskään luottaisi niiden
generoimiin testeihin.

## Syötteet tekoälylle

I was to create a web user interface for the rock, paper, scissors application.
This is a Python project built using Poetry. Reuse as much of the current code
as possible. Player number one is always a human player. Player two can be a
human player or an AI.

Good. The web page opens and user can choose the mode. I noticed that in pvp
mode, the 2nd player can (visually) see the move the 1st player has made. This
should not happen.

Great! In the player vs AI modes, it seems that the AI always makes the same
move. This happens because a new game object is created for each move. The game
objects should be persisted (in memory).

Fix the syntax errors in get_tuomari function.

Now there's some syntax errors in make_move function.

Remove the console application (index.py) and create automated tests for the web
application. All the tests in the project should pass.

Update the functionality so that each game is played until one player has
reached five wins. Add test cases for this new feature. All the test cases
should still pass.

The pvp mode seems to be broken. None of the moves are registered.

That did not seem to fix the issue.

(Tekoäly ei pystynyt korjaamaan tätä virhettä. Sen suoritus näytti jäävän jumiin
pytest-ajoon. Korjasin virheen käsin.)

Extract getting the game_type from session and converting it into Pelityyppi
object into helper functgion (sic).
