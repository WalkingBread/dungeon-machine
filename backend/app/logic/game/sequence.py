from dataclasses import dataclass

from app.logic.game.scene import Scene
from app.logic.game.state import GameState


@dataclass
class StorySequence:
    scene: Scene
    player_action: str
