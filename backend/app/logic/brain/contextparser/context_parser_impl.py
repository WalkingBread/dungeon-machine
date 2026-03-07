from logic.brain.contextparser.context_parser import ContextParser
from logic.character.stat import Statistics
from logic.game.character import GameCharacter
from logic.game.game import GameState
from logic.game.player_action import PlayerAction, DiceRollActionState
from logic.game.scene import Scene


class ContextParserImpl(ContextParser):

    def parse_to_scene_setting_context(self, story: list[Scene], game_state: GameState) -> dict:
        """
        Helper to extract the most recent scene and common state data.
        """
        last_scene = story[-1] if story else Scene()

        return {
            "players": [self._character_to_dict(c) for c in game_state.player_characters],
            "game_characters": [self._character_to_dict(c) for c in game_state.npc_characters],
            "previous_scene_content": last_scene.get_scene_content(),
        }

    def parse_to_player_action_outcome_context(self, story: list[Scene], player_actions: list[PlayerAction],
                                               game_state: GameState) -> dict:
        """
        Prepares data specifically for the LLM to decide on dice rolls and
        consequences based on the player's last move.
        """
        current_scene = story[-1] if story else Scene()

        return {
            "player characters": [self._character_to_dict(c) for c in game_state.player_characters],
            "player actions": [self._serialize_player_action(a) for a in player_actions],
            "npc characters": [self._character_to_dict(c) for c in game_state.npc_characters],
            "current scene content": current_scene.get_scene_content(),
        }

    def _serialize_player_action(self, action: PlayerAction) -> dict:
        """
        Serializes the action with a focus on the 'Unresolved' elements
        to prompt the LLM for the next logic step.
        """
        completed_rolls = [
            {
                "stat": r.statistic.name if r.statistic else "General",
                "result": r.dice_result.name if r.dice_result else "Unknown",
                "description": r.result_description
            }
            for r in action.dice_rolls if r.state == DiceRollActionState.FINISHED
        ]

        active_roll = None
        if action.dice_rolls and action.dice_rolls[-1].state != DiceRollActionState.FINISHED:
            last = action.dice_rolls[-1]
            active_roll = {
                "stat": last.statistic.name if last.statistic else "General",
                "result": last.dice_result.name if last.dice_result else "Waiting for roll...",
                "current_roll_state": last.state.name
            }

        return {
            "player": action.player_name,
            "overall_state": action.state.name,
            "player_intent": action.player_action,
            "completed_steps": completed_rolls,
            "active_event": active_roll,
        }

    def _character_to_dict(self, character: GameCharacter) -> dict:
        if not character:
            return {}

        char_data = {
            "name": getattr(character, 'name', "Unknown"),
            "health": f"{getattr(character, 'health', 0)}/{getattr(character, 'max_health', 0)}",
        }

        money = getattr(character, 'money', 0)
        if money:
            char_data["money"] = money

        stats = getattr(character, 'stats', None)
        if stats:
            serialized_stats = self._serialize_statistics(stats)
            if serialized_stats:
                char_data["stats"] = serialized_stats

        return char_data

    def _serialize_statistics(self, statistics: Statistics) -> dict:
        if not statistics or not hasattr(statistics, 'stats'):
            return {}

        return {
            stat_type.name: stat_obj._value
            for stat_type, stat_obj in statistics.stats.items()
        }