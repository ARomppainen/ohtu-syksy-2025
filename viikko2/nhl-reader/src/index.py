import requests
from typing import List
from player import Player

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    response = requests.get(url).json()

    players: List[Player]  = []

    for player_dict in response:
        player = Player(**player_dict)
        players.append(player)

    print("Players from FIN:")

    for player in players:
        if player.nationality == 'FIN':
            print(player)

if __name__ == "__main__":
    main()
