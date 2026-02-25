from abc import ABC, abstractmethod

from logic.game.scene import SceneSchema
from logic.game.action import PlayerAction, PlayerActionEvents
from logic.modelmanager.context import GameContext

class ModelManager(ABC):
    @abstractmethod
    def provide_scene_description(self, game_context: GameContext) -> SceneSchema:
        pass

    @abstractmethod
    def provide_character_events(self, player_action: PlayerAction) -> PlayerActionEvents:
        pass