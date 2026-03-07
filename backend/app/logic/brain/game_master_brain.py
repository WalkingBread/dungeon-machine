from logic.brain.contextparser.context_parser_impl import ContextParserImpl
from logic.brain.modelmanager.model_manager import ModelManager
from logic.brain.responseparser.response_parser import ResponseParser
from logic.brain.player_action_outcome import PlayerActionOutcome
from logic.game.game import GameState
from logic.game.game_event import GameEvent
from logic.game.player_action import PlayerAction
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
        return GameIntroductionSequence(content="The village of Oakhaven was promised to be a respite from the mud and blood of the High Road. But as the sun dips below the jagged peaks of the Spine, the long shadows seem to pull at your heels. The air here is too quiet—no crickets chirp, and the locals bar their doors before the light is even gone. You each find yourselves in The Crow’s Nest tavern, not because of the cheap ale, but because it’s the only hearth still burning. As a heavy, rhythmic thudding begins beneath the floorboards, you realize that whatever is haunting this town isn't coming from the woods. It’s already inside'")

    def provide_scene_setting(self, history: list[Scene], game_state: GameState) \
            -> tuple[SceneDescriptionSequence, list[GameEvent]]:

        context = self._context_parser.parse_to_scene_setting_context(history, game_state)
        story_update = self._model_manager.provide_scene_setting(context)
        return self._response_parser.parse_to_scene_setting(story_update)

    def provide_player_actions_outcome(self, history: list[Scene], actions: list[PlayerAction], game_state: GameState) \
            -> list[PlayerActionOutcome]:

        context = self._context_parser.parse_to_player_action_outcome_context(history, actions, game_state)
        action_outcomes = self._model_manager.provide_player_action_outcome(context)
        return self._response_parser.parse_to_player_action_outcome(action_outcomes)
