from dataclasses import dataclass, field
from typing import List

from logic.character.stat import StatType

@dataclass(frozen=True)
class GameMasterRequest:
    player_name: str

@dataclass(frozen=True)
class PlayerInputRequest(GameMasterRequest):
    text: str

@dataclass(frozen=True)
class PlayerInputResponse:
    player_name: str
    player_action: str

@dataclass(frozen=True)
class DiceRollRequest(GameMasterRequest):
    statistic: StatType | None

@dataclass(frozen=True)
class DiceRollResponse:
    player_name: str
    roll_value: int

@dataclass(frozen=True)
class GameMasterResponse:
    narrative: str

@dataclass(frozen=True)
class GameIntroduction(GameMasterResponse):
    pass

@dataclass(frozen=True)
class SceneIntroduction(GameMasterResponse):
    roll_requests: List[DiceRollRequest] = field(default_factory=list)
    input_requests: List[PlayerInputRequest] = field(default_factory=list)

@dataclass(frozen=True)
class PlayerActionSegment(GameMasterResponse):
    request: GameMasterRequest = None