from __future__ import annotations
from dataclasses import dataclass
from typing import TYPE_CHECKING

from logic.character import Character
from logic.game.player import Player

if TYPE_CHECKING:
    from logic.game import Game

@dataclass
class CharacterData:
    name: str

    @classmethod
    def from_character(cls, character: Character):
        return cls(character.name)

    @classmethod
    def from_characters(cls, characters: list[Character]):
        return [cls.from_character(c) for c in characters]
    
    def to_dict(self) -> dict:
        return {
            'name': self.name
        }

@dataclass
class PlayerData:
    name: str

    @classmethod
    def from_player(cls, player: Player):
        return cls(player.name)

    @classmethod
    def from_players(cls, players: list[Player]):
        return [cls.from_player(p) for p in players]
    
    def to_dict(self) -> dict:
        return {
            'name': self.name
        }

@dataclass
class GameState:
    characters: list[CharacterData]
    players: list[PlayerData]

    @classmethod
    def capture_state(cls, game: Game):
        return cls(
            CharacterData.from_characters(game.characters),
            PlayerData.from_players(game.players)
        )
    
    def to_dict(self) -> dict:
        return {
            'characters': [c.to_dict() for c in self.characters],
            'players': [p.to_dict() for p in self.players]
        }
