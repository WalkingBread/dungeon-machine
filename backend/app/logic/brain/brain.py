import logging
from enum import Enum
from typing import Callable

from logic.brain.model.manager import ModelManager
from logic.game.game import GameState
from logic.game.player_action import PlayerAction
from logic.game.scene import Scene
from logic.brain.dtos import SceneIntroductionDto, DiceRollRequestDto, FinalActionOutcomeDto
from logic.brain.context.parser import (
    PlayerActionParser,
    SceneSettingParser,
    RollOutcomeParser
)
from logic.brain.response.parser import (
    StoryUpdateParser,
    ActionDecisionParser,
    RollRequirementParser,
    RollConsequenceParser,
    FinalSummaryParser
)

class ContextParser(Enum):
    SCENE_SETTING = SceneSettingParser()
    PLAYER_ACTION = PlayerActionParser()
    ROLL_OUTCOME = RollOutcomeParser()

class ResponseParser(Enum):
    STORY_UPDATE = StoryUpdateParser()
    ACTION_DECISION = ActionDecisionParser()
    ROLL_REQUIREMENT = RollRequirementParser()
    ROLL_CONSEQUENCE  = RollConsequenceParser()
    FINAL_SUMMARY = FinalSummaryParser()


class GameMasterBrain:
    """
    GMB is a component responsible for orchestrating context parser, model manager and response parser.
    It receives the objects familiar to GameMaster and handles its parsing into LLM familiar dtos
    for the model manager, it returns its own dtos which usually store strings and sometimes game events.
    """
    def __init__(self):
        self._model_manager = ModelManager()

    def _dispatch(self, context_parser: ContextParser, model_call: Callable, 
                      response_parser: ResponseParser, *args):
        context = context_parser.value.parse(*args)
        raw_response = model_call(context)
        return response_parser.value.parse(raw_response)

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
        return self._dispatch(
            ContextParser.SCENE_SETTING,
            self._model_manager.provide_scene_setting,
            ResponseParser.STORY_UPDATE,
            story, game_state
        )

    def does_the_action_continue(self, story: list[Scene], action: PlayerAction, game_state: GameState) -> bool:
        return self._dispatch(
            ContextParser.PLAYER_ACTION,
            self._model_manager.provide_action_decision,
            ResponseParser.ACTION_DECISION,
            story, action, game_state
        )

    def provide_required_roll(self, story: list[Scene], action: PlayerAction, game_state: GameState) -> DiceRollRequestDto:
        return self._dispatch(
            ContextParser.PLAYER_ACTION,
            self._model_manager.provide_action_roll,
            ResponseParser.ROLL_REQUIREMENT,
            story, action, game_state
        )

    def provide_roll_outcome_desc(self, story: list[Scene], action: PlayerAction, game_state: GameState) -> str:
        return self._dispatch(
            ContextParser.ROLL_OUTCOME,
            self._model_manager.provide_action_roll_outcome_description,
            ResponseParser.ROLL_CONSEQUENCE,
            story, action, game_state
        )

    def provide_final_action_outcome(self, story: list[Scene], action: PlayerAction, game_state: GameState) -> FinalActionOutcomeDto:
        return self._dispatch(
            ContextParser.PLAYER_ACTION,
            self._model_manager.provide_action_final_summary,
            ResponseParser.FINAL_SUMMARY,
            story, action, game_state
        )