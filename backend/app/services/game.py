from logic.game.session import SessionManager, GameSession, Player
from uuid import UUID
from functools import wraps

SESSION_MAX_PLAYER_COUNT = 4

class SessionNotFoundError(Exception):
    def __init__(self, session_id: str):
        super().__init__(f'Session of id {session_id} was not found.')

class SessionFullError(Exception):
    def __init__(self, session_id: str):
        super().__init__(f'Session of id {session_id} is full.')

class InvalidUsernameError(Exception):
    def __init__(self, username: str):
        super().__init__(f'Username {username} is invalid.')

class PlayerNotFoundError(Exception):
    def __init__(self, player_id: str):
        super().__init__(f'Player of id {player_id} was not found.')

class PlayersNotReadyError(Exception):
    def __init__(self):
        super().__init__('Not all players are ready.')

def _is_valid_username(username: str) -> bool:
    # TO DO
    return True

def validate_session(func):
    @wraps(func)
    def wrapper(self, session_id, *args, **kwargs):
        session = self._session_manager.get_session(UUID(session_id))
        
        if not session:
            raise SessionNotFoundError(session_id)
        
        return func(self, session, *args, **kwargs)
    return wrapper

def validate_player(func):
    @wraps(func)
    def wrapper(self, session: GameSession, player_id: str, *args, **kwargs):
        player = session.get_player(UUID(player_id))
        
        if not player:
            raise PlayerNotFoundError(player_id)
        
        return func(self, session, player, *args, **kwargs)
    return wrapper

class GameService:
    def __init__(self, session_manager: SessionManager):
        self._session_manager = session_manager

    def create_game(self) -> GameSession:
        return self._session_manager.create_session()
    
    def _get_session(self, session_id: str) -> GameSession:
        return self._session_manager.get_session(UUID(session_id))

    @validate_session
    def join_game(self, session: GameSession, username: str):
        if session.player_count >= SESSION_MAX_PLAYER_COUNT:
            raise SessionFullError(session.id)
        
        if not _is_valid_username(username):
            raise InvalidUsernameError(username)
        
        return session.join(username)
        
    @validate_session
    def start_game(self, session: GameSession, game_theme: str):
        success = session.start_game(game_theme)
        if not success:
            raise PlayersNotReadyError()
        
    @validate_session
    @validate_player
    def create_character(self, session: GameSession, player: Player, name: str):
        return session.create_character(player, name)
