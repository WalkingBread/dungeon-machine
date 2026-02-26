from abc import ABC, abstractmethod

from logic.game.game import GameState
from logic.game.game_event import GameEvent
from logic.game.scene import SceneDescriptionSequence, ActionDescriptionSequence, Scene


class GameMasterBrain(ABC):
    """
    GameMasterBrain servers as the LLM pipeline orchestrator.
    """

    @abstractmethod
    def get_game_introduction(self, theme: str = None):
        pass

    @abstractmethod
    def provide_scene_setting(self, history: list[Scene], game_state: GameState) \
            -> tuple[SceneDescriptionSequence, list[GameEvent]]:
        pass

    @abstractmethod
    def provide_action_reaction(self, history: list[Scene], game_state: GameState) \
            -> tuple[ActionDescriptionSequence, list[GameEvent]]:
        pass