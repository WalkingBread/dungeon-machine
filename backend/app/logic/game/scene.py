from dataclasses import dataclass

from logic.game.event import GameEvent
from logic.game.state import GameState

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
    
    def to_dict(self):
        return {
            'narrative': self.narrative,
            'events_invoked_at_scene': [e.to_dict() for e in self.schema.events],
            'game_state_after_events': self.game_state.to_dict()
        }