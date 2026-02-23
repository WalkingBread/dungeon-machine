from app.logic.game import Scene, Game
from app.logic.game.state import GameState
from app.logic.game.sequence import Sequence
from app.logic.player import Player

class GameMaster:
    def __init__(self):
        self.game = None
        self.previous_sequences = []

    def create_game(self, theme: str, players: list[Player]):
        self.game = Game(theme, players)

    def introduce_story(self):
        # generate scene
        # execute generated events in game
        # ask for player action
        # create sequence
        pass

    def provide_next_scene(self):
        # take last sequence 
        # generate scene based on it
        # ask for player action
        # create sequence
        pass

    def _capture_game_state(self):
        pass


        