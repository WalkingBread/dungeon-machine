from dataclasses import dataclass

from app.logic.game import Scene
from app.logic.game.state import GameState

@dataclass
class Sequence:
    scene: Scene
    game_state: GameState
    player_action: str