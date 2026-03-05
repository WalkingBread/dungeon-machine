from logic.game import GameMaster
from logic.game.character import PlayerCharacter
from enum import Enum
import uuid

class PlayerNotJoinedError(Exception):
    def __init__(self, player: Player):
        super().__init__(f'Player {player.username} has not joined the game.')

class PlayerStatus(Enum):
    CREATING_CHARACTER = 'Creating character...'
    READY = 'Ready.'

class Player:
    def __init__(self, id: str, username: str):
        self._id = id
        self.username = username
        self.status = PlayerStatus.CREATING_CHARACTER

    @property
    def id(self):
        return self._id

    @property
    def ready(self):
        return self.status is PlayerStatus.READY

class GameSession:
    def __init__(self, id: str):
        self._id = id
        self._game_master = GameMaster()
        self._players: dict[str, Player] = {}
        self._player_characters: dict[str, PlayerCharacter] = {}

    @property
    def id(self):
        return self._id

    @property
    def game_master(self):
        return self._game_master

    @property
    def game_started(self) -> bool:
        return self.game_master.game is not None
    
    @property
    def players_ready(self) -> bool:
        for p in self._players.values():
            if not p.ready:
                return False
        return True
    
    @property
    def player_count(self):
        return len(self._players)
    
    def get_player(self, player_id):
        return self._players[player_id]
    
    def create_character(self, player: Player, name: str) -> PlayerCharacter:
        if player not in self._players.values():
            raise PlayerNotJoinedError(player)
        
        character = PlayerCharacter.generate_character(name)
        self._player_characters[player.id] = character
        player.status = PlayerStatus.READY
        return character

    def join(self, username) -> Player:
        player_id = str(uuid.uuid4())
        player = Player(player_id, username)
        self._players[player_id] = player
        return player
        
    def start_game(self, game_theme):
        if not self.game_started and self.players_ready:
            self.game_master.create_game(
                game_theme, 
                self._player_characters.values()
            )
            return True
        return False
    
class SessionManager:
    def __init__(self):
        self._sessions: dict[str, GameSession] = {}

    def create_session(self) -> GameSession:
        session_id = str(uuid.uuid4())
        session = GameSession(session_id)
        self._sessions[session_id] = session
        return session
    
    def get_session(self, id: str):
        return self._sessions[id]