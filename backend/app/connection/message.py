from enum import Enum, auto

class MessageType(str, Enum):    
    def _generate_next_value_(name, _start, _count, _last_values):
        return name.upper()
    
    PLAYER_JOINED = auto()
    PLAYER_LEFT = auto()
    CHARACTER_CREATED = auto()
    GAME_STARTED = auto()
    AUTHENTICATE = auto()
    SESSION_STATE = auto()
    INFO = auto()
    ERROR = auto()