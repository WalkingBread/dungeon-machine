from app.logic.dice import D10
from app.logic.dice import get_dice_for, RollType
from enum import Enum, auto

from typing import Callable

class StatType(Enum):
    def _generate_next_value_(name, _start, _count, _last_values):
        return name.upper()
    STRENGTH = auto()
    AGILITY = auto()
    INTELLIGENCE = auto()
    LUCK = auto()
    CHARISMA = auto()

class Statistic:
    def __init__(self, value: int):
        self._value = value
        self.max_value = get_dice_for(RollType.STAT).sides

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

    def __repr__(self):
        lines = [f"  {s.name.title():<12} : {inst.value:>3}" for s, inst in self.stats.items()]
        return "Statistics:\n" + "\n".join(lines)
    
    def upgrade_stat(self, stat_type: StatType, value: int = 1):
        self.stats[stat_type] += value

    @classmethod
    def roll_stats(cls, creation_method: Callable[[], Statistic]):
        return cls({s: creation_method() for s in StatType})
    
def warhmamer_stat_creation_method() -> Statistic:
    dice = D10()
    rolls = [dice.roll() for _ in range(2)]
    return Statistic(sum(rolls) + 20)

