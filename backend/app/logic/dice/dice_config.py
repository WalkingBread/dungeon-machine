from math import ceil, floor
from enum import Enum, auto
from dataclasses import dataclass
from app.logic.dice.dice import D100, D20, D8, D6, D4

class RollType(Enum):
    STAT = auto()
    INITIATIVE = auto()

class TestRollOutcome(Enum):
    EXTREME_SUCCESS = auto()
    SUCCESS = auto()
    FAILURE = auto()
    EXTREME_FAILURE = auto()

    @classmethod
    def get_outcome(cls, roll_value: int, pass_value: int, roll_type: RollType = None):
        is_success = roll_value <= pass_value
        
        if roll_type not in TEST_ROLL_CONFIG:
            return TestRollOutcome.SUCCESS if is_success else TestRollOutcome.FAILURE

        extreme_roll_conf = TEST_ROLL_CONFIG[roll_type] 
        dice = ROLL_TYPE_DICE_CONFIG[roll_type]

        if is_success:
            if extreme_roll_conf.is_extreme_success(roll_value, dice.sides):
                return TestRollOutcome.EXTREME_SUCCESS
            return TestRollOutcome.SUCCESS
        
        else:
            if extreme_roll_conf.is_extreme_failure(roll_value, dice.sides):
                return TestRollOutcome.EXTREME_FAILURE
            return TestRollOutcome.FAILURE
        
class Percent:
    def __init__(self, value: float):
        self._value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value: float):
        self._value = max(0.0, min(float(new_value), 1.0))

    def __repr__(self):
        return f"{self._value * 100:.1f}%"
    
@dataclass
class ExtremeRollConfig:
    extreme_success_p: Percent
    extreme_failure_p: Percent

    def is_extreme_success(self, roll: int, sides: int) -> bool:
        return roll <= ceil(self.extreme_success_p.value * sides)

    def is_extreme_failure(self, roll: int, sides: int) -> bool:
        return roll >= floor((1.0 - self.extreme_failure_p.value) * sides) + 1

    @classmethod
    def set(cls, extreme_success_percent: float, exteme_failure_percent: float):
        return cls(
            Percent(extreme_success_percent), 
            Percent(exteme_failure_percent)
        )
    
TEST_ROLL_CONFIG = {
    RollType.STAT: ExtremeRollConfig.set(0.05, 0.05),
}

ROLL_TYPE_DICE_CONFIG = {
    RollType.STAT: D100(),
    RollType.INITIATIVE: D20()
}

def get_dice_for(roll_type: RollType):
    return ROLL_TYPE_DICE_CONFIG[roll_type]