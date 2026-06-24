from logic.game.character import PlayerCharacter, NonPlayableCharacter, GameCharacter
from logic.game.event import GameEvent
from logic.game.event.handler import EventHandlerManager
from logic.game.scene import EngineEventSequence

from dataclasses import dataclass


class Game:
    def __init__(self, theme: str, player_characters: list[PlayerCharacter]):
        self.theme = theme
        self.player_characters = player_characters
        self.npcs = []

        self._event_handler_manager = EventHandlerManager(self)

    @property
    def characters(self) -> list[GameCharacter]:
        return self.player_characters + self.npcs
    
    def _get_character(self, name: str, characters: list[GameCharacter]) -> GameCharacter:
        for character in characters:
            if character.name == name:
                return character
            
    def get_character(self, name: str):
        return self._get_character(name, self.characters)
            
    def get_player_character(self, name: str) -> PlayerCharacter:
        return self._get_character(name, self.player_characters)
    
    def get_npc(self, name: str) -> NonPlayableCharacter:
        return self._get_character(name, self.npcs)

    def execute_events(self, events: list[GameEvent]) -> list[EngineEventSequence]:
        if not events:
            return []

        sequences = []

        for event in events:
            self._event_handler_manager.handle_event(event)

            description = event.to_description()
            sequences.append(EngineEventSequence(description))

        return sequences

    def capture_game_state(self) -> GameState:
        return GameState(self.theme, self.player_characters, self.npcs)

@dataclass(frozen=True)
class GameState:
    theme: str
    player_characters: list[PlayerCharacter]
    npc_characters: list[NonPlayableCharacter]