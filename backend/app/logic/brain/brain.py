from enum import Enum
from typing import Callable

from logic.brain.model.manager import ModelManager
from logic.game.game import GameState
from logic.game.player_action import PlayerAction
from logic.game.scene import Scene
from logic.brain.dto.brain import SceneIntroductionDto, DiceRollRequestDto, FinalActionOutcomeDto
from logic.brain.context.parser import (
    PlayerActionParser,
    SceneSettingParser,
    RollOutcomeParser,
    StoryThemeParser
)
from logic.brain.response.parser import (
    StoryUpdateParser,
    StoryIntroParser,
    ActionDecisionParser,
    RollRequirementParser,
    RollConsequenceParser,
    FinalSummaryParser
)

class ContextParser(Enum):
    STORY_THEME = StoryThemeParser()
    SCENE_SETTING = SceneSettingParser()
    PLAYER_ACTION = PlayerActionParser()
    ROLL_OUTCOME = RollOutcomeParser()

class ResponseParser(Enum):
    STORY_INTRO = StoryIntroParser()
    STORY_UPDATE = StoryUpdateParser()
    ACTION_DECISION = ActionDecisionParser()
    ROLL_REQUIREMENT = RollRequirementParser()
    ROLL_CONSEQUENCE  = RollConsequenceParser()
    FINAL_SUMMARY = FinalSummaryParser()


"""
GMB is a component responsible for orchestrating context parser, model manager and response parser.
It receives the objects familiar to GameMaster and handles its parsing into LLM familiar dtos
for the model manager, it returns its own dtos which usually store strings and sometimes game events.
"""
class GameMasterBrain:
    def __init__(self):
        self._model_manager = ModelManager()

    def _dispatch(self, context_parser: ContextParser, model_call: Callable, 
                      response_parser: ResponseParser, *args):
        context = context_parser.value.parse(*args)
        raw_response = model_call(context)
        return response_parser.value.parse(raw_response)

    def provide_game_introduction(self, story_theme: str) -> str:
        return self._dispatch(
            ContextParser.STORY_THEME,
            self._model_manager.provide_story_intro,
            ResponseParser.STORY_INTRO,
            story_theme
        )

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