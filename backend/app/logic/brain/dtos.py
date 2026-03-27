from dataclasses import dataclass, field

from logic.brain.model.request_structures import StatisticType
from logic.game.game_event import GameEvent

# Those are the dtos sent to GameMaster after GMB is called
# We also use strings and bools which don't have explicit dtos

@dataclass(frozen=True)
class SceneIntroductionDto:
    scene_intro: str
    game_events: list[GameEvent] = field(default_factory=list)

@dataclass(frozen=True)
class DiceRollRequestDto:
    attempt_desc: str
    requested_stat: StatisticType | None = None

@dataclass(frozen=True)
class FinalActionOutcomeDto:
    outcome_desc: str
    game_events: list[GameEvent] = field(default_factory=list)

