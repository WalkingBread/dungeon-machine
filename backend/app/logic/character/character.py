from app.logic.character.inventory import Inventory
from app.logic.character.stat import Statistics, StatType, warhmamer_stat_creation_method
from app.logic.dice.dice import Dice
from app.logic.dice.dice_config import RollType, TestRollOutcome, get_dice_for
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

    def roll_dice(self, dice: Dice, modifier: int = 0) -> int:
        roll = dice.roll()
        return dice.normalize_value(roll + modifier)

    def test_roll(self, roll_type: RollType, pass_value: int, modifier: int = 0) -> TestRollOutcome:
        dice = get_dice_for(roll_type)
        roll = self.roll_dice(dice, modifier)
        return TestRollOutcome.get_outcome(roll, pass_value, roll_type)

    def roll_for_stat(self, stat: StatType, modifier: int = 0) -> TestRollOutcome:
        return self.test_roll(RollType.STAT, self.stats[stat], modifier)

    @classmethod
    def generate_character(cls, name: str):
        stats = Statistics.roll_stats(warhmamer_stat_creation_method)
        return cls(name, stats)
    
ch1 = Character.generate_character('aaa')
print(ch1.stats.strength)
