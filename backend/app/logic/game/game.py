from logic.game.characters import PlayerManagedCharacter, GameManagedCharacter
from logic.game.game_event import GameEvent
from dataclasses import dataclass

from logic.game.scene import EngineEventSequence


class Game:
    def __init__(self, theme: str, players: list[PlayerManagedCharacter]):
        self.theme = theme
        self.players = players
        self.characters = []

    def execute_events(self, events: list[GameEvent]) -> list[EngineEventSequence]:
        """
        will update the state of the players and characters, empty for now
        """
        return [EngineEventSequence(e.event_str) for e in events]

    def capture_game_state(self) -> GameState:
        return GameState(self.theme, self.players, self.characters)

@dataclass(frozen=True)
class GameState:
    theme: str
    players: list[PlayerManagedCharacter]
    characters: list[GameManagedCharacter]