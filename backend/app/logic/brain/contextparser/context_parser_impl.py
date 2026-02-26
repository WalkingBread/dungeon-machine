from dataclasses import asdict

from logic.brain.contextparser.context_parser import ContextParser
from logic.game.game import GameState
from logic.game.scene import Scene


class ContextParserImpl(ContextParser):

    def parse_to_scene_setting_context(self, history: list[Scene], game_state: GameState) -> dict:
        """
        Helper to extract the most recent scene and common state data.
        """
        current_scene = history[-1] if history else Scene()

        return {
            "theme": game_state.theme,
            "players": [asdict(p) for p in game_state.players],
            "characters": [asdict(c) for c in game_state.characters],
            "previous_scene_content": current_scene.get_scene_content(),
        }

    def parse_to_action_reaction_context(self, history: list[Scene], game_state: GameState) -> dict:
        """
        Prepares data specifically for the LLM to decide on dice rolls and
        consequences based on the player's last move.
        """
        current_scene = history[-1] if history else Scene()

        return {
            "theme": game_state.theme,
            "players": [asdict(p) for p in game_state.players],
            "characters": [asdict(c) for c in game_state.characters],
            "current_scene_content": current_scene.get_scene_content(),
        }