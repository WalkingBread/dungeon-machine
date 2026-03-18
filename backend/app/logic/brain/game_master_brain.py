import logging

from logic.brain.contextparser.context_parser import ContextParser
from logic.brain.modelmanager.model_manager import ModelManager
from logic.brain.responseparser.response_parser import ResponseParser
from logic.game.game import GameState
from logic.game.player_action import PlayerAction
from logic.game.scene import Scene
from logic.brain.dtos import SceneIntroductionDto, DiceRollRequestDto, FinalActionOutcomeDto


class GameMasterBrain:
    """
    GMB is a component responsible for orchestrating context parser, model manager and response parser.
    It receives the objects familiar to GameMaster and handles its parsing into LLM familiar dtos
    for the model manager, it returns its own dtos which usually store strings and sometimes game events.
    """
    def __init__(self):
        self._context_parser = ContextParser()
        self._model_manager = ModelManager()
        self._response_parser = ResponseParser()

    def provide_game_introduction(self, theme: str = None) -> str:
        """
        Generates the initial world-building parameters based on a theme.
        Mocking this for now.
        """
        return (
            """The sun is warm on your backs as you walk into the village of Oakhaven. 
The town square is a mess of colorful ribbons, wooden stalls, and the delicious smell
of cooling pies. Today is the Annual Blackberry Festival, and everyone is in
a great mood—except for Old Man Miller.

Miller, the town’s most famous baker, is standing by his empty stall, looking pale. 
He’s supposed to present the "Crown Tart" to the Mayor in exactly one hour to 
officially start the feast. The problem? The tart is gone.
            """)

    def provide_scene_intro(self, story: list[Scene], game_state: GameState) -> SceneIntroductionDto:
        context = self._context_parser.parse_to_scene_setting_context(story, game_state)
        story_update = self._model_manager.provide_scene_setting(context)
        return self._response_parser.parse_story_update(story_update)

    def does_the_action_continue(self, story: list[Scene], action: PlayerAction, game_state: GameState) -> bool:
        context = self._context_parser.parse_to_player_action_context(story, action, game_state)
        decision = self._model_manager.provide_action_decision(context)
        return self._response_parser.parse_action_decision(decision)

    def provide_required_roll(self, story: list[Scene], action: PlayerAction, game_state: GameState) -> DiceRollRequestDto:
        context = self._context_parser.parse_to_player_action_context(story, action, game_state)
        roll_requirement = self._model_manager.provide_action_roll(context)
        return self._response_parser.parse_roll_requirement(roll_requirement)

    def provide_roll_outcome_desc(self, story: list[Scene], action: PlayerAction, game_state: GameState) -> str:
        context = self._context_parser.parse_to_roll_outcome_context(story, action, game_state)
        desc = self._model_manager.provide_action_roll_outcome_description(context)
        return desc.desc

    def provide_final_action_outcome(self, story: list[Scene], action: PlayerAction, game_state: GameState) -> FinalActionOutcomeDto:
        context = self._context_parser.parse_to_player_action_context(story, action, game_state)
        final_summary = self._model_manager.provide_action_final_summary(context)
        return self._response_parser.parse_final_summary(final_summary)

