from app.logic.character.inventory import Inventory
from app.logic.character.stat import Statistics, StatType
from app.logic.dice.dice import D100

INVENTORY_SIZE = 10
MAX_HEALTH = 15

STAT_DICE = D100()

class Character:
    def __init__(self, name: str, stats: Statistics, 
                 inventory_size: int = INVENTORY_SIZE, 
                 max_health: int = MAX_HEALTH):
        self.name = name
        self.max_health = max_health
        self.health = max_health
        self.money = 0
        self.stats = stats
        self.inventory = Inventory(inventory_size)

    def roll_for_stat(stat: StatType, modifier: int = 0):
        roll = STAT_DICE.roll()
        return STAT_DICE.normalize_value(roll + modifier)