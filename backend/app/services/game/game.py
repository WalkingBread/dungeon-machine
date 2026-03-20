from logic.game.session import SessionManager, GameSession, Player
from services.game.error import (
    SessionNotFoundError, 
    SessionFullError, 
    PlayersNotReadyError, 
    PlayerNotFoundError,
    PlayerAuthenticationError,
    InvalidUsernameError
)
from uuid import UUID
from functools import wraps

SESSION_MAX_PLAYER_COUNT = 4

def _is_valid_username(username: str) -> bool:
    # TO DO
    return True

def validate_session(func):
    @wraps(func)
    def wrapper(self, session_id: UUID, *args, **kwargs):
        session = self._get_session(session_id)
        
        if not session:
            raise SessionNotFoundError(session_id)
        
        return func(self, session, *args, **kwargs)
    return wrapper

def validate_player(func):
    @wraps(func)
    def wrapper(self, session: GameSession, player_id: UUID, *args, **kwargs):
        player = session.get_player(player_id)
        
        if not player:
            raise PlayerNotFoundError(player_id)
        
        return func(self, session, player, *args, **kwargs)
    return wrapper

def authenticate_player(func):
    @wraps(func)
    def wrapper(self, session: GameSession, player: Player, 
                auth_token: str, *args, **kwargs):
        if auth_token != player.auth_token:
            raise PlayerAuthenticationError(player.id)
        
        return func(self, session, player, *args, **kwargs)
    return wrapper

class GameService:
    def __init__(self, session_manager: SessionManager):
        self._session_manager = session_manager

    def create_game(self) -> GameSession:
        return self._session_manager.create_session()
    
    @validate_session
    def get_session(self, session: GameSession) -> GameSession:
        return session
    
    def _get_session(self, session_id: UUID) -> GameSession:
        return self._session_manager.get_session(session_id)
    
    @validate_session
    @validate_player
    @authenticate_player
    def auth_player(self, session: GameSession, player: Player):
        return player

    @validate_session
    def join_game(self, session: GameSession, username: str):
        if session.player_count >= SESSION_MAX_PLAYER_COUNT:
            raise SessionFullError(session.id)
        
        if not _is_valid_username(username):
            raise InvalidUsernameError(username)
        
        return session.join(username)
    
    @validate_session
    @validate_player
    @authenticate_player
    def leave_game(self, session: GameSession, player: Player):
        session.leave(player)
        
    @validate_session
    def start_game(self, session: GameSession, game_theme: str):
        success = session.start_game(game_theme)
        if not success:
            raise PlayersNotReadyError()
        
    @validate_session
    @validate_player
    @authenticate_player
    def create_character(self, session: GameSession, player: Player, name: str):
        return session.create_character(player, name)
