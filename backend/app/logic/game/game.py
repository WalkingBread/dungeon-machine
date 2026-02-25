from logic.game.character import NPC, Player
from logic.game.scene import SceneSchema, Scene
from logic.game.action import PlayerActionEvents
from logic.game.state import GameState

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logic.game.event import GameEvent

class Game:
    def __init__(self, theme: str, players: list[Player]):
        self.theme = theme
        self.players = players
        self.characters: list[NPC] = []

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
    
    def spawn_character(self, name: str):
        self.characters.append(
            NPC.generate_character(name)
        )

    def remove_character(self, character: NPC):
        self.characters.remove(character)
    
    def capture_game_state(self) -> GameState:
        return GameState.capture_state(self)
