from typing import Any
from matchers import All, And, HasAtLeast, HasFewerThan, Matcher, PlaysIn


class QueryBuilder:
    def __init__(self, matcher: Matcher | None = None):
        self._query: Matcher = All() if matcher is None else matcher

    def build(self) -> Matcher:
        return self._query

    def plays_in(self, team: str) -> "QueryBuilder":
        return QueryBuilder(And(self._query, PlaysIn(team)))

    def has_at_least(self, value: Any, attr: str):
        return QueryBuilder(And(self._query, HasAtLeast(value, attr)))

    def has_fewer_than(self, value: Any, attr: str):
        return QueryBuilder(And(self._query, HasFewerThan(value, attr)))
