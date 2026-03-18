from logic.game.game_master import GameMaster
from logic.game.character import PlayerCharacter
from enum import Enum
from uuid import uuid4, UUID

class PlayerNotJoinedError(Exception):
    def __init__(self, player: Player):
        super().__init__(f'Player {player.username} has not joined the game.')

class CharacterAlreadyCreatedError(Exception):
    def __init__(self, player: Player):
        super().__init__(f'Player {player.username} has already created a character.')

class PlayerNotInGameError(Exception):
    def __init__(self, player: Player):
        super().__init__(f'Player {player.username} is not present in the game.')

class PlayerStatus(Enum):
    CREATING_CHARACTER = 'Creating character...'
    READY = 'Ready.'

class Player:
    def __init__(self, id: UUID, username: str):
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
    def __init__(self, id: UUID):
        self._id = id
        self._game_master = GameMaster()
        self._players: dict[UUID, Player] = {}
        self._player_characters: dict[UUID, PlayerCharacter] = {}

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
    
    def get_player(self, player_id: UUID):
        return self._players.get(player_id)
    
    def create_character(self, player: Player, name: str) -> PlayerCharacter:
        if player.id not in self._players:
            raise PlayerNotJoinedError(player)
        
        if player.id in self._player_characters:
            raise CharacterAlreadyCreatedError(player)
        
        character = PlayerCharacter.generate_character(name)
        self._player_characters[player.id] = character
        player.status = PlayerStatus.READY
        return character

    def join(self, username) -> Player:
        player_id = uuid4()
        player = Player(player_id, username)
        self._players[player_id] = player
        return player
    
    def leave(self, player: Player):
        player = self._players.pop(player.id, None)
        if player is None:
            raise PlayerNotInGameError(player)

        self._player_characters.pop(player.id, None)

        
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
        self._sessions: dict[UUID, GameSession] = {}

    def create_session(self) -> GameSession:
        session_id = uuid4()
        session = GameSession(session_id)
        self._sessions[session_id] = session
        return session
    
    def get_session(self, id: UUID):
        return self._sessions.get(id)