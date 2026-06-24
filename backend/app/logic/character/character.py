from logic.character.inventory import Inventory
from logic.character.item import Item
from logic.character.stat import Statistics, StatType, warhmamer_stat_creation_method
from logic.dice import Dice, RollType, TestRollOutcome, get_dice_for

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

    @property
    def stats_dict(self) -> dict[str, int]:
        return self.stats.to_dict()

    def roll_dice(self, dice: Dice, modifier: int = 0, normalize_outcome: bool = True) -> int:
        roll = dice.roll()
        modified_roll = roll + modifier
        return dice.normalize(modified_roll) if normalize_outcome else modified_roll
    
    def _test_roll(self, roll_type: RollType, pass_value: int, modifier: int = 0) -> tuple[int, TestRollOutcome]:
        dice = get_dice_for(roll_type)
        roll_value = self.roll_dice(dice, modifier, True)
        return roll_value, TestRollOutcome.get_outcome(roll_value, pass_value, roll_type)

    def roll_for_stat(self, stat: StatType, modifier: int = 0) -> tuple[int, TestRollOutcome]:
        return self._test_roll(RollType.STAT, self.stats[stat], modifier)
    
    def roll_for_initiative(self, modifier: int = 0) -> int:
        dice = get_dice_for(RollType.INITIATIVE)
        return self.roll_dice(dice, modifier, False)
    
    def pickup_item(self, item: Item):
        success = self.inventory.add_item(item)
        return success
    
    def drop_item(self, item: Item):
        self.inventory.remove_item(item)

    def change_health(self, hp_change: int):
        self.health += hp_change
        self.health = max(0, min(self.health, self.max_health))

    @classmethod
    def generate_character(cls, name: str):
        stats = Statistics.roll_stats(warhmamer_stat_creation_method)
        return cls(name, stats)