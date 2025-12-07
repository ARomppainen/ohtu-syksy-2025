from player_reader import PlayerReader
from player_statistics import Statistics
from matchers import All, And, HasAtLeast, HasFewerThan, Not, Or, PlaysIn
from query_builder import QueryBuilder


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

    query = QueryBuilder()
    matcher = (
        query.plays_in("NYR")
        .has_at_least(10, "goals")
        .has_fewer_than(20, "goals")
        .build()
    )

    print("result of 7th query")
    for player in stats.matches(matcher):
        print(player)
    print()

    matcher = query.one_of(
        query.plays_in("PHI").has_at_least(10, "assists").has_fewer_than(10, "goals"),
        query.plays_in("EDM").has_at_least(50, "points"),
    ).build()

    print("result of 8th query")
    for player in stats.matches(matcher):
        print(player)
    print()


if __name__ == "__main__":
    main()
