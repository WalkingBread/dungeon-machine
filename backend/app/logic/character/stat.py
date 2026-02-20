from app.logic.dice.dice import Dice
from enum import Enum, auto

class StatType(Enum):
    STRENGTH = auto(),
    AGILITY = auto(),
    INTELLIGENCE = auto(),
    LUCK = auto(), 
    CHARISMA = auto()

class Statistic:
    def __init__(self, value: int, max_value: int):
        self._value = value
        self.max_value = max_value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: int):
        self._value = max(1, min(value, self.max_value))

class Statistics:
    def __init__(self, stats: dict[StatType, Statistic]):
        self.stats = stats

    def __getitem__(self, key: StatType):
        return self.stats[key].value
    
    def __getattr__(self, name: str):
        try:
            key = StatType[name.upper()]
            return self.stats[key].value
        except KeyError:
            raise AttributeError(f"'Statistics' object has no attribute '{name}'")
        
    def __setattr__(self, name: str, value: int):
        if name == "stats":
            super().__setattr__(name, value)
        else:
            try:
                key = StatType[name.upper()]
                self.stats[key].value = value
            except KeyError:
                super().__setattr__(name, value)

    @classmethod
    def roll_stats(cls, dice: Dice):
        return cls({s: Statistic(dice.roll(), dice.sides) for s in StatType})
    