from queue import Queue
from app.models.event import Event

class GameState:
    _game_state = None
    def __init__(self, player_chars: list, game_log: list[str]) -> GameState:
        if (GameState._game_state is not None):
            raise Exception("The game state is already instantiated")
        self.player_chars = player_chars
        self.gamelog = game_log
        self._event_queue = Queue()
        GameState._game_state = self

    @classmethod
    def get_game_state(cls):
        if(GameState._game_state is None):
            GameState()
        return cls._game_state
    
    def publish_to_event_queue(self, event: Event):
        self._event_queue.put(event)


    