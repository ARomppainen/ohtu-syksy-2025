# GitHub Copilotin tekemä koodikatselmointi

https://github.com/ARomppainen/ohtu-syksy-2025/pull/1

## Mitä huomioita Copilot teki?

Copilot teki monta huomiota liittyen metodien paluuarvojen puuttuvaan staattiseen tyypitykseen.
Nämä olivat kaikki ihan valideja, joten otin ne mukaan.

Tärkein Copilotin huomio oli funktionaalinen muutos, minkä olin tehnyt metodiin `won_point`.
Metodissa on verrataan metodiparametria `player_name` vakioon `player1` riippumatta pelaajien
nimistä. Tämä on hieman hämmentävää, joten olin muuttanut metodin toimintaa vertaamaan
sitä konstruktorissa annettuun arvoon. Tämä on ns. breaking change luokan julkisen rajapinnan
toimintaan, joten päätin palauttaa metodin alkuperäisen toiminnan. Muutin kuitenkin parametrin
nimen `player_name` -> `player` ja lisäsin tälle staattisen tyypityksen `Literal['player1', 'player2']`.

Kolmas huomio liityi kahden apumetodin parametrin `player: PlayerNumber` tyypitykseen. PlayerNumber on
alias tyypille `Literal[1,2]`. Codepilot ehdotti, että tähän voisi lisätä validaatiota tai tämän
voisi muuttaa `IntEnum` tyyppiseksi dokumentaation parantamiseksi. Yhtään monimutkaisemmassa
tapauksessa `IntEnum` olisi paikallaan (varsinkin jos kyseessä olisi luokan julkinen rajapinta),
mutta 'type safetyä' se ei kuitenkaan parantaisi.

Muita havaintoja Copilot ei tehnyt. Koin ehdotetut muutokset ihan asiallisiksi.
