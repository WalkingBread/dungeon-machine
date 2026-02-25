from logic.game.game import Game
from logic.game.scene import Scene, SceneSchema
from logic.game.sequence import StorySequence
from logic.game.player import Player
from logic.game.action import PlayerAction, PlayerActionEvents
from logic.modelmanager.context import GameContext
from logic.game.state import GameState, PlayerData

from logic.modelmanager import ModelManager

class GameMaster:
    def __init__(self, brain: ModelManager):
        self._game: Game = None
        self._history: list[StorySequence] = []
        self.current_scene: Scene = None
        self.player_actions: list[PlayerActionEvents] = []

        self.brain = brain

    @property
    def game(self):
        return self._game
    
    @property
    def last_sequence(self) -> StorySequence:
        return self._history[-1] if self._history else None
    
    def create_game(self, theme: str, players: list[Player]):
        self._game = Game(theme, players)

    def introduce_story(self) -> Scene:
        scene_schema = self._fetch_story_introduction()
        self.current_scene = self._game.build_scene(scene_schema)
        return self.current_scene
    
    def provide_scene(self) -> Scene:
        self._end_current_scene()
        scene_schema = self._fetch_next_scene()
        self.current_scene = self.game.build_scene(scene_schema)
        return self.current_scene
    
    def _end_current_scene(self):
        self._history.append(StorySequence(
            self.current_scene,
            self.player_actions
        ))
        self.current_scene = None
        self.player_actions = []
    
    def execute_player_action(self, player: Player, action: str) -> GameState:
        player_action = PlayerAction(
            PlayerData.from_player(player), 
            action
        )
        action_events = self._fetch_player_action_events(player_action)
        return self.game.execute_player_action_events(action_events)
        
    def _get_game_context(self) -> GameContext:
        return GameContext(
            self.game.capture_game_state(),
            self.last_sequence
        )

    def _fetch_next_scene(self) -> SceneSchema:
        return self.brain.provide_scene_description(
            self._get_game_context()
        )

    def _fetch_story_introduction(self) -> SceneSchema:
        return SceneSchema(
            "The village of Oakhaven was promised to be a respite from the mud and blood of the High Road. But as the sun dips below the jagged peaks of the Spine, the long shadows seem to pull at your heels. The air here is too quiet—no crickets chirp, and the locals bar their doors before the light is even gone. You each find yourselves in The Crow’s Nest tavern, not because of the cheap ale, but because it’s the only hearth still burning. As a heavy, rhythmic thudding begins beneath the floorboards, you realize that whatever is haunting this town isn't coming from the woods. It’s already inside'",
            []
        )

    def _fetch_player_action_events(self, player_action: PlayerAction) -> PlayerActionEvents:
        return self.brain.provide_character_events(player_action)