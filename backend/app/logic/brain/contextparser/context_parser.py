from abc import ABC, abstractmethod

from logic.game.game import GameState
from logic.game.scene import Scene


class ContextParser(ABC):
    @abstractmethod
    def parse_to_scene_setting_context(self, history: list[Scene], game_state: GameState) -> dict:
        pass

    @abstractmethod
    def parse_to_player_action_outcome_context(self, history: list[Scene], game_state: GameState) -> dict:
        pass