from logic.game.character import PlayerCharacter, GameCharacter, NonPlayableCharacter
from logic.game.game_event import GameEvent
from dataclasses import dataclass

from logic.game.scene import EngineEventSequence


class Game:
    def __init__(self, theme: str, player_characters: list[PlayerCharacter]):
        self.theme = theme
        self.player_characters = player_characters
        self.npc_characters = []

    def execute_events(self, events: list[GameEvent]) -> list[EngineEventSequence]:
        """
        will update the state of the players and characters, empty for now
        """
        return [EngineEventSequence(e.event_str) for e in events]

    def capture_game_state(self) -> GameState:
        return GameState(self.theme, self.player_characters, self.npc_characters)

@dataclass(frozen=True)
class GameState:
    theme: str
    player_characters: list[PlayerCharacter]
    npc_characters: list[NonPlayableCharacter]