from app.logic.game import Game
from app.logic.game.scene import Scene, SceneSchema
from app.logic.game.sequence import StorySequence
from app.logic.game.player import Player
from app.logic.game.action import PlayerAction, PlayerActionEvents
from app.logic.game.state import GameState

class GameMaster:
    def __init__(self):
        self._game: Game = None
        self._scene_history: list[Scene] = []

    @property
    def game(self):
        return self._game
    
    def create_game(self, theme: str, players: list[Player]):
        self._game = Game(theme, players)

    @property
    def last_sequence(self) -> StorySequence:
        return self.history[-1] if self.history else None
    
    def provide_scene(self) -> Scene:
        scene_schema = self._fetch_next_scene()
        return self.game.build_scene(scene_schema)
    
    def execute_player_action(self, player: Player, action: str) -> GameState:
        player_action = PlayerAction(player, action)
        

    def _fetch_next_scene(self) -> SceneSchema:
        pass

    def _fetch_player_action_events(self, player_action: PlayerAction) -> PlayerActionEvents:
        pass