from dataclasses import dataclass, field

from logic.brain.model.request import StatisticType
from logic.game.event import GameEvent

@dataclass(frozen=True)
class SceneIntroductionDto:
    scene_intro: str
    game_events: list[GameEvent] = field(default_factory=list)

@dataclass(frozen=True)
class SceneDescriptionDto:
    description: str
    game_events: list[GameEvent] = field(default_factory=list)

@dataclass(frozen=True)
class ActionStateDto:
    narrative: str
    state: str
    game_events: list[GameEvent] = field(default_factory=list)

@dataclass(frozen=True)
class DiceRollRequestDto:
    requested_stat: StatisticType | None = None

@dataclass(frozen=True)
class FinalActionDescDto:
    desc: str