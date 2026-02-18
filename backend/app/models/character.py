from dataclasses import dataclass
from app.logic.character.inventory import Inventory

@dataclass
class Character:
    name: str
    description: str
    health: int
    strength: int
    agility: int
    intelligence: int
    luck: int
    charisma: int
    money: int
    # inventory: Inventory


