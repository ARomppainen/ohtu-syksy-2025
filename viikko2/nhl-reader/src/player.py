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
    
    def __str__(self):
        return f"{self.name} team {self.team} goals {self.goals} assists {self.assists}"
