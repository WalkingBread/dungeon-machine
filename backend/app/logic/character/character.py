from app.logic.character.inventory import Inventory
from app.logic.character.stat import Statistics, StatType
from app.logic.dice.dice import Dice
from app.logic.character.dice_config import RollType, TestRollOutcome, get_dice_for

INVENTORY_SIZE = 10
MAX_HEALTH = 15

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

    def roll_dice(self, dice: Dice, modifier: int = 0):
        roll = dice.roll()
        return dice.normalize_value(roll + modifier)

    def roll_for_stat(self, stat: StatType, modifier: int = 0):
        dice = get_dice_for(RollType.STAT)
        roll = self.roll_dice(dice, modifier)
        return TestRollOutcome.get_outcome(roll, self.stats[stat])

    @classmethod
    def generate_character(cls, name: str):
        dice = get_dice_for(RollType.STAT)
        stats = Statistics.roll_stats(dice)
        return cls(name, stats)

