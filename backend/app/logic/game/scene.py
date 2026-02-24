from dataclasses import dataclass

from app.logic.game.event import GameEvent
from app.logic.game.state import GameState

@dataclass
class SceneSchema:
    narrative: str
    events: list[GameEvent]

@dataclass
class Scene:
    schema: SceneSchema
    game_state: GameState

    @property
    def narrative(self) -> str:
        return self.schema.narrative