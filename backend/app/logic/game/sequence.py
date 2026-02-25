from dataclasses import dataclass

from logic.game.scene import Scene
from logic.game.action import PlayerActionEvents

@dataclass
class StorySequence:
    scene: Scene
    player_actions: list[PlayerActionEvents]

    def to_dict(self):
        return {
            'scene': self.scene.to_dict(),
            'player_actions': [p.to_dict() for p in self.player_actions]
        }