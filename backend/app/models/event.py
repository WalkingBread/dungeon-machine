from dataclasses import dataclass
from enum import Enum, auto
from app.logic.character.stat import StatType

class EventType(Enum):
    DICE_EVENT = auto()
    HEALTH_EVENT = auto()

@dataclass
class Event:
    event_type: EventType

@dataclass
class DiceEvent(Event):
    player_name: str
    related_attribute: StatType

@dataclass
class HealthEvent(Event):
    player_name: str
    value_change: str