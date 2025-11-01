from dataclasses import dataclass


@dataclass
class Player:
    id: int
    name: str
    nationality: str
    team: str
    assists: int
    goals: int
    games: int

    @property
    def points(self) -> int:
        return self.goals + self.assists

    def __str__(self):
        return f"{self.name:22} {self.team:16} {self.goals:2} + {self.assists:2} = {self.points:2}"
