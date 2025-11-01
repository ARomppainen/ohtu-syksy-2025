from typing import List

from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

from player import Player
from player_reader import PlayerReader
from player_stats import PlayerStats


def players_table(players: List[Player], season: str, nationality: str) -> Table:
    """Create a table with list of players"""
    table = Table(title=f"[italic]Season {season} players from {nationality}[/italic]")
    table.add_column("Released", style="dim cyan")
    table.add_column("teams", style="magenta")
    table.add_column("goals", style="dim green")
    table.add_column("assists", style="dim green")
    table.add_column("points", style="dim green")
    for player in players:
        table.add_row(
            player.name,
            player.team,
            str(player.goals),
            str(player.assists),
            str(player.points),
        )
    return table


def main():
    console = Console()
    prompt = Prompt()

    seasons = [f"20{xx}-{xx+1}" for xx in range(18, 26)]
    season = prompt.ask("Season", choices=seasons, default="2024-25")

    url = f"https://studies.cs.helsinki.fi/nhlstats/{season}/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    nationalities = stats.nationalities()
    while True:
        nationality = prompt.ask("Nationality", choices=nationalities, default="")
        players = stats.top_scorers_by_nationality(nationality)
        table = players_table(players, season, nationality)
        console.print(table)


if __name__ == "__main__":
    main()
