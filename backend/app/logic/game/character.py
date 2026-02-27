from dataclasses import dataclass
from abc import ABC


@dataclass
class Character(ABC):
    character_id: int
    name: str
    description: str
    health_points: int

@dataclass
class PlayerCharacter(Character):
    pass

@dataclass
class GameCharacter(Character):
    pass