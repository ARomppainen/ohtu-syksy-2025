from abc import ABC
from typing import Any
from player import Player


class Matcher(ABC):
    def test(self, player: Player) -> bool: ...


class All(Matcher):
    def test(self, player: Player):
        return True


class And(Matcher):
    def __init__(self, *matchers: Matcher):
        self._matchers = matchers

    def test(self, player: Player) -> bool:
        return all(m.test(player) for m in self._matchers)


class Or(Matcher):
    def __init__(self, *matchers: Matcher):
        self._matchers = matchers

    def test(self, player: Player) -> bool:
        return any(m.test(player) for m in self._matchers)


class Not(Matcher):
    def __init__(self, matcher: Matcher):
        self._matcher = matcher

    def test(self, player: Player) -> bool:
        return not self._matcher.test(player)


class PlaysIn(Matcher):
    def __init__(self, team: str):
        self._team = team

    def test(self, player: Player) -> bool:
        return player.team == self._team


class HasAtLeast(Matcher):
    def __init__(self, value: Any, attr: str):
        self._value = value
        self._attr = attr

    def test(self, player: Player) -> bool:
        player_value = getattr(player, self._attr)

        return player_value >= self._value


class HasFewerThan(HasAtLeast):

    def test(self, player: Player) -> bool:
        return not super().test(player)
