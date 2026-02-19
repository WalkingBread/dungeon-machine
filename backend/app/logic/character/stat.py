from dataclasses import dataclass, fields
from app.logic.dice.dice import D100

STAT_DICE = D100()

class Statistic:
    def __init__(self, value: int):
        self._value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value: int):
        self._value = max(1, min(value, STAT_DICE.sides))

@dataclass
class Statistics:
    health: Statistic
    strength: Statistic
    agility: Statistic
    intelligence: Statistic
    luck: Statistic
    charisma: Statistic
    money: Statistic

    @classmethod
    def roll_stats(cls):
        stats_dict = {f.name: Statistic(STAT_DICE.roll()) for f in fields(cls)}
        return cls(**stats_dict)
    