from logic.game.player import Player
from logic.game.event import GameEvent
from logic.game.scene import SceneSchema, Scene
from logic.game.action import PlayerActionEvents
from logic.game.state import GameState

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
        # todo
        return self.execute_events(action_events.events)

    def execute_events(self, events: list[GameEvent]) -> GameState:
        # todo
        # execute events
        return self.capture_game_state()
    
    def capture_game_state(self) -> GameState:
        return GameState.capture_state(self)
