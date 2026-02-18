from dataclasses import dataclass
from logic.character.inventory import Inventory

@dataclass
class Character:
    name: str
    health: int
    strength: int
    agility: int
    intelligence: int
    luck: int
    charisma: int
    money: int
    inventory: Inventory


