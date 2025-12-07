from statistics import Statistics
from player_reader import PlayerReader
from matchers import All, And, HasAtLeast, HasFewerThan, Not, Or, PlaysIn


def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)

    matcher = And(HasAtLeast(5, "goals"), HasAtLeast(20, "assists"), PlaysIn("PHI"))

    print("result of 1st query")
    for player in stats.matches(matcher):
        print(player)
    print()

    matcher = And(Not(HasAtLeast(2, "goals")), PlaysIn("NYR"))

    print("result of 2nd query")
    for player in stats.matches(matcher):
        print(player)
    print()

    matcher = And(HasFewerThan(2, "goals"), PlaysIn("NYR"))

    print("result of 3rd query")
    for player in stats.matches(matcher):
        print(player)
    print()

    print("result of 4th query")
    filtered_with_all = stats.matches(All())
    print(len(filtered_with_all))
    print()

    matcher = Or(HasAtLeast(45, "goals"), HasAtLeast(70, "assists"))
    print("result of 5th query")
    for player in stats.matches(matcher):
        print(player)
    print()

    matcher = And(
        HasAtLeast(70, "points"), Or(PlaysIn("COL"), PlaysIn("FLA"), PlaysIn("BOS"))
    )

    print("result of 6th query")
    for player in stats.matches(matcher):
        print(player)
    print()


if __name__ == "__main__":
    main()
