from enum import Enum, auto

class DiceType(str, Enum):
    def _generate_next_value_(name, _start, _count, _last_values):
        return name.upper()
    D4 = auto()
    D6 = auto()
    D10 = auto()
    D20 = auto()
    D100 = auto()