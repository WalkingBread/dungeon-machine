from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from typing import Optional


@dataclass
class Character(ABC):
    character_id: int
    name: str
    description: str
    health_points: int

@dataclass
class PlayerManagedCharacter(Character):
    pass

@dataclass
class GameManagedCharacter(Character):
    pass