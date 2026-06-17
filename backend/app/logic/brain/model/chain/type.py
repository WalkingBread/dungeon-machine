from enum import Enum, auto

class ChainType(Enum):
    DECIDER = auto()
    ROLL_SETTER = auto()
    ROLL_OUTCOME = auto()
    FINALIZER = auto()
    STORY_INTRO = auto()
    STORY_UPDATE = auto()