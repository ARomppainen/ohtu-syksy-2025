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

    print("Players from FIN\n")

    filtered = filter(lambda p: p.nationality == 'FIN', players)

    for player in sorted(filtered, key=lambda p: p.score, reverse=True):
        print(player)

if __name__ == "__main__":
    main()
