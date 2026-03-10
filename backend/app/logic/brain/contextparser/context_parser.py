from abc import ABC, abstractmethod

from logic.game.game import GameState
from logic.game.player_action import PlayerAction
from logic.game.scene import Scene


class ContextParser(ABC):
    @abstractmethod
    def parse_to_scene_setting_context(self, history: list[Scene], game_state: GameState) -> dict:
        pass

    @abstractmethod
    def parse_to_player_action_context(
            self,
            story: list[Scene],
            player_action: PlayerAction,
            game_state: GameState
    ) -> dict:
        """
        Orchestrates all parsing logic to create the payload for the
        LLM action chains (DECIDER, ROLL_SETTER, etc.).
        """