from app.logic.game.state import PlayerData
from app.logic.game.event import GameEvent
from dataclasses import dataclass

@dataclass
class PlayerAction:
    player: PlayerData
    action: str


@dataclass
class PlayerActionEvents:
    player_action: PlayerAction
    events: list[GameEvent]

    @property
    def action(self):
        return self.player_action.action
    
    