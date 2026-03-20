from logic.game.character import PlayerCharacter, NonPlayableCharacter
from logic.game.game_event import GameEvent
from dataclasses import dataclass

from logic.game.handlers import EVENT_HANDLERS
from logic.game.scene import EngineEventSequence


class Game:
    def __init__(self, theme: str, player_characters: list[PlayerCharacter]):
        self.theme = theme
        self.player_characters = player_characters
        self.npc_characters = []

    def execute_events(self, events: list[GameEvent]) -> list[EngineEventSequence]:
        if not events:
            return []

        sequences = []

        for event in events:
            handler = EVENT_HANDLERS.get(type(event))
            if handler:
                handler(self, event)

            description = event.to_description()
            sequences.append(EngineEventSequence(description))

        return sequences

    def capture_game_state(self) -> GameState:
        return GameState(self.theme, self.player_characters, self.npc_characters)

@dataclass(frozen=True)
class GameState:
    theme: str
    player_characters: list[PlayerCharacter]
    npc_characters: list[NonPlayableCharacter]