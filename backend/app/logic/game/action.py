from logic.game.state import PlayerData
from dataclasses import dataclass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logic.game.event import GameEvent

@dataclass
class PlayerAction:
    player: PlayerData
    action: str

    def to_dict(self) -> dict:
        return {
            'player': self.player.to_dict(),
            'action': self.action
        }


@dataclass
class PlayerActionEvents:
    player_action: PlayerAction
    events: list[GameEvent]

    @property
    def action(self):
        return self.player_action.action
    
    @property
    def player(self):
        return self.player_action.player
    
    def to_dict(self) -> dict:
        return {
            'player': self.player.to_dict(),
            'action': self.action,
            'events': [e.to_dict() for e in self.events]
        }
    
    