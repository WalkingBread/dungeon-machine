from uuid import UUID

class SessionNotFoundError(Exception):
    def __init__(self, session_id: UUID):
        super().__init__(f'Session of id {str(session_id)} was not found.')

class SessionFullError(Exception):
    def __init__(self, session_id: UUID):
        super().__init__(f'Session of id {str(session_id)} is full.')

class InvalidUsernameError(Exception):
    def __init__(self, username: str):
        super().__init__(f'Username {username} is invalid.')

class PlayerNotFoundError(Exception):
    def __init__(self, player_id: UUID):
        super().__init__(f'Player of id {str(player_id)} was not found.')

class PlayerAuthenticationError(Exception):
    def __init__(self, player_id: UUID):
        super().__init__(f'Wrong authentication token for player {str(player_id)}.')

class PlayersNotReadyError(Exception):
    def __init__(self):
        super().__init__('Not all players are ready.')