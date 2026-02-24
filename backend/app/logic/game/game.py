from app.logic.game.player import Player
from app.logic.game.state import GameState
from app.logic.game.event import GameEvent
from app.logic.game.scene import SceneSchema, Scene
from app.logic.game.action import PlayerActionEvents

class Game:
    def __init__(self, theme: str, players: list[Player]):
        self.theme = theme
        self.players = players
        self.characters = []

    def build_scene(self, scene_schema: SceneSchema) -> Scene:
        return Scene(
            scene_schema,
            self.execute_events(scene_schema.events)
        )
    
    def execute_player_action_events(self, action_events: PlayerActionEvents) -> GameState:
        return self.execute_events(action_events.events)

    def execute_events(self, events: list[GameEvent]) -> GameState:
        # execute events
        return self._capture_game_state()
    
    def _capture_game_state(self) -> GameState:
        return GameState.capture_state(self)

