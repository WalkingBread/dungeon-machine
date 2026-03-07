from dataclasses import dataclass
from logic.game.game_event import GameEvent

@dataclass
class PlayerActionOutcome:
    player_name: str
    outcome_description: str
    game_events: list[GameEvent] = None

    @property
    def is_final_outcome(self) -> bool:
        if self.game_events:
            for event in self.game_events:
                if hasattr(event, 'require_player_input') and event.require_player_input:
                    return True
        return False
