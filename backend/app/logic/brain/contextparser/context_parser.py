import json

from logic.brain.contextparser.decorators import require_player_context, require_story_context
from logic.character.stat import Statistics
from logic.game.character import GameCharacter
from logic.game.game import GameState
from logic.game.player_action import PlayerAction, ActionVerificationException
from logic.game.scene import Scene


class ContextParser:

    @require_story_context
    def parse_to_scene_setting_context(self, story: list[Scene], game_state: GameState) -> dict:
        """
        Helper to extract the most recent scene and common state data for the new scene prompt.
        """
        scene_content = story[-1].get_scene_content()
        serialized_game_state = self._parse_game_state(game_state)

        return {
            "scene": scene_content,
            "game_state": serialized_game_state,
        }

    @require_story_context
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
        scene_content = story[-1].get_scene_content()
        serialized_game_state = self._parse_game_state(game_state)

        intent_context = self._parse_player_intent(player_action)
        action_history_context = self._parse_action_history(player_action)

        return {
            "scene": scene_content,
            "game_state": serialized_game_state,
            "intent": intent_context,
            "action_history": action_history_context
        }

    @require_story_context
    def parse_to_roll_outcome_context(
            self,
            story: list[Scene],
            player_action: PlayerAction,
            game_state: GameState
    ) -> dict:
        """
        A separate parsing method for getting roll outcome description.
        It needs additional parameter (result)
        """
        action_context = self.parse_to_player_action_context(story, player_action, game_state)
        action_context["result"] = player_action.last_dice_roll.dice_result.name

        return action_context

    def _serialize_statistics(self, statistics: Statistics) -> dict:
        if not statistics or not hasattr(statistics, 'stats'):
            return {}

        return {
            stat_type.name: stat_obj._value
            for stat_type, stat_obj in statistics.stats.items()
        }

    def _parse_character_to_json(self, character: GameCharacter) -> str:
        """
        Serializes a single GameCharacter into a JSON string for LLM consumption.
        Reuses existing serialization logic for consistency.
        """
        stats_data = self._serialize_statistics(character.stats)

        character_map = {
            "name": getattr(character, 'name', "Unknown"),
            "health": f"{getattr(character, 'health', 0)}/{getattr(character, 'max_health', 0)}",
            "statistics": stats_data
        }

        compact_json = json.dumps(character_map, indent=None, separators=(',', ':'))

        return compact_json + "\n"

    def _parse_game_state(self, game_state: GameState) -> str:
        """
        Serializes a GameState into a categorized Markdown + JSONL string.
        """
        output = []

        output.append("#### PLAYER_CHARACTERS")
        if not game_state.player_characters:
            output.append("None")
        else:
            for pc in game_state.player_characters:
                output.append(self._parse_character_to_json(pc).strip())
        output.append("")

        output.append("#### GAME_CHARACTERS")
        if not game_state.npc_characters:
            output.append("None")
        else:
            for npc in game_state.npc_characters:
                output.append(self._parse_character_to_json(npc).strip())

        return "\n".join(output) + "\n"

    @require_player_context
    def _parse_action_history(self, action: PlayerAction) -> str:
        history_lines = []

        for i, roll in enumerate(action.dice_rolls, 1):
            stat_name = roll.statistic.name if roll.statistic else "NO_STATISTIC"

            line_parts = [f"ROLL {i} ({stat_name})"]

            if roll.attempt_description:
                line_parts.append(f"- Attempt: {roll.attempt_description}")

            if roll.dice_result:
                line_parts.append(f"| Result: {roll.dice_result.name}")

            if roll.result_description:
                line_parts.append(f"| Outcome: {roll.result_description}")

            history_lines.append(" ".join(line_parts))

        if action.result_description:
            history_lines.append(f"FINAL SUMMARY: {action.result_description}")

        return "\n".join(history_lines)

    @require_player_context
    def _parse_player_intent(self, action: PlayerAction) -> str:
        clean_intent = action.player_action.strip()

        return f"Player {action.player_name.strip()} wants to: {clean_intent}"
