from app.logic.player import Player
from app.logic.game.state import GameState

class Game:
    def __init__(self, theme: str, players: list[Player]):
        self.theme = theme
        self.players = players
        self.characters = []

