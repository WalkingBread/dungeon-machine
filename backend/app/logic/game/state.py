from dataclasses import dataclass
from app.logic.character import Character
from app.logic.player import Player
from app.logic.game import Game, Scene

@dataclass
class CharacterData:
    name: str

    @classmethod
    def from_character(cls, character: Character):
        return cls(character.name)

    @classmethod
    def from_characters(cls, characters: list[Character]):
        return [cls.from_character(c) for c in characters]

@dataclass
class PlayerData:
    name: str

    @classmethod
    def from_player(cls, player: Player):
        return cls(player.name)

    @classmethod
    def from_players(cls, players: list[Player]):
        return [cls.from_player(p) for p in players]

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