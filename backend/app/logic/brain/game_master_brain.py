import logging

from logic.brain.contextparser.context_parser_impl import ContextParserImpl
from logic.brain.modelmanager.model_manager import ModelManager
from logic.brain.responseparser.response_parser import ResponseParser
from logic.game.game import GameState
from logic.game.game_event import GameEvent, DiceEvent
from logic.game.player_action import PlayerAction, PlayerActionState, ActionVerificationException, DiceRollActionState
from logic.game.scene import SceneDescriptionSequence, Scene, GameIntroductionSequence

class GameMasterBrain:
    def __init__(self):
        self._context_parser = ContextParserImpl()
        self._model_manager = ModelManager()
        self._response_parser = ResponseParser()

    def get_game_introduction(self, theme: str = None) -> GameIntroductionSequence:
        """
        Generates the initial world-building parameters based on a theme.
        Mocking this for now.
        """
        return GameIntroductionSequence(content=(
            "Oakhaven is glowing under a warm orange sunset. "
            "Friendly skeletons in colorful vests are busy sweeping the streets and hanging lanterns. "
            "You step into 'The Golden Flagon' tavern. It smells like fresh bread and honey ale. "
            "A skeleton with a tiny chef's hat is juggling plates, and a magical harp plays a bouncy tune. "
            "The skeletal barkeep, Barnaby, clinks his wooden mug against the counter and whistles through his teeth to welcome you."
        ))

    def provide_scene_setting(self, history: list[Scene], game_state: GameState) \
            -> tuple[SceneDescriptionSequence, list[GameEvent]]:

        context = self._context_parser.parse_to_scene_setting_context(history, game_state)
        story_update = self._model_manager.provide_scene_setting(context)
        return self._response_parser.parse_to_scene_setting(story_update)

    def process_player_action_outcome(self, story: list[Scene], action: PlayerAction, game_state: GameState) \
            -> list[GameEvent]:

        context = self._context_parser.parse_to_player_action_context(story, action, game_state)

        match action.state:
            case PlayerActionState.REQUIRES_DESCRIPTION:
                # 1. Handle Dice Roll Outcome Narrative
                if action.last_dice_roll and action.last_dice_roll.state == DiceRollActionState.REQUIRES_DESCRIPTION:
                    result_name = action.last_dice_roll.dice_result.name
                    context["result"] = result_name

                    print(f"[BRAIN] Generating narrative for dice result: {result_name}")
                    roll_cnsq = self._model_manager.provide_action_roll_outcome_description(context)

                    print(f"[BRAIN] Outcome Description: {roll_cnsq.desc}")
                    action.add_roll_description(roll_cnsq.desc)

                    # Refresh context to include the new narrative we just added
                    context = self.get_new_context(story, action, game_state)

                # 2. Decision Phase
                print(f"[BRAIN] Invoking Decider for action: '{action.player_action}'")
                dice_dec = self._model_manager.provide_action_decision(context)
                print(f"[BRAIN] Decider result: {dice_dec.decision}")

                # 3. Execution Phase
                if dice_dec.decision == "FINISH":
                    print("[BRAIN] Finalizing action and generating summary...")
                    final_sum = self._model_manager.provide_action_final_summary(context)

                    print(f"[BRAIN] Final Story: {final_sum.final_story}")
                    print(f"[BRAIN] Events generated: {final_sum.final_events}")

                    action.add_final_description(final_sum.final_story)
                    return self._response_parser.map_to_game_events(final_sum.final_events)

                else:
                    print("[BRAIN] Action continues. Requesting new roll...")
                    dice_roll = self._model_manager.provide_action_roll(context)

                    stat = self._response_parser.map_stat_type(dice_roll.statistic)
                    print(f"[BRAIN] New Roll Required: {stat.name} | Intro: {dice_roll.intro}")

                    action.add_new_dice_roll(stat, dice_roll.intro)
                    return [DiceEvent(player_name=action.player_name, statistic=stat)]
            case _:
                raise ActionVerificationException(f"Unhandled Brain state: {action.state}")

    def get_new_context(self, story: list[Scene], action: PlayerAction, game_state: GameState):
        return self._context_parser.parse_to_player_action_context(
            story, action, game_state
        )
