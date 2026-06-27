from dataclasses import dataclass

from logic.character.stat import StatType
from logic.dice import TestRollOutcome

@dataclass(frozen=True)
class NarrativeSegment:
    text: str

@dataclass(frozen=True)
class PlayerInputRequest:
    player_name: str
    text: str

@dataclass(frozen=True)
class PlayerInputResponse:
    player_name: str
    player_action: str

@dataclass(frozen=True)
class PlayerDiceRollRequest:
    player_name: str
    statistic: StatType | None

@dataclass(frozen=True)
class PlayerDiceRollResponse:
    player_name: str
    roll_value: int