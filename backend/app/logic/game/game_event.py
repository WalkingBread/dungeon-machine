from abc import ABC, abstractmethod
from dataclasses import dataclass
from logic.character.character import StatType
from logic.dice import TestRollOutcome

@dataclass
class GameEvent(ABC):
    @abstractmethod
    def to_description(self) -> str:
        pass

@dataclass
class HealthEvent(GameEvent):
    character_name: str
    health_change: int

    def to_description(self) -> str:
        if self.health_change == 0:
            return f"{self.character_name}'s health remained unchanged."

        verb = "gained" if self.health_change > 0 else "lost"
        amount = abs(self.health_change)

        return f"{self.character_name} {verb} {amount} health points."

@dataclass
class AddCharacterEvent(GameEvent):
    character_name: str
    health_points: int

    def to_description(self) -> str:
        return f"A character named \"{self.character_name}\" has entered the scene!"

@dataclass
class RemoveCharacterEvent(GameEvent):
    character_name: str

    def to_description(self) -> str:
        return f"{self.character_name} has disappeared from the scene."