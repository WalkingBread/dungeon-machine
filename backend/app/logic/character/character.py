from app.logic.character.inventory import Inventory, WarhammerInventory
from app.logic.character.item import Item
from app.logic.character.stat import Statistics, StatType, warhmamer_stat_creation_method, warhammer_stat_bonus
from app.logic.dice.dice import Dice
from app.logic.dice.dice_config import RollType, TestRollOutcome, get_dice_for
from app.logic.character.status import Status 


INVENTORY_SIZE = 10
INVENTORY_WEIGHT_LIMIT = 50
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
        self.inventory = Inventory(inventory_size,INVENTORY_WEIGHT_LIMIT)
        self.statuses = set()

    def roll_dice(self, dice: Dice, modifier: int = 0, normalize_outcome: bool = True) -> int:
        roll = dice.roll()
        modified_roll = roll + modifier
        return dice.normalize_value(modified_roll) if normalize_outcome else modified_roll
    
    def _test_roll(self, roll_type: RollType, pass_value: int, modifier: int = 0) -> TestRollOutcome:
        dice = get_dice_for(roll_type)
        roll_value = self.roll_dice(dice, modifier, True)
        return TestRollOutcome.get_outcome(roll_value, pass_value, roll_type)

    def roll_for_stat(self, stat: StatType, modifier: int = 0) -> TestRollOutcome:
        return self._test_roll(RollType.STAT, self.stats[stat], modifier)
    
    def roll_for_initiative(self, modifier: int = 0) -> int:
        dice = get_dice_for(RollType.INITIATIVE)
        return self.roll_dice(dice, modifier, False)
    
    def pickup_item(self, item: Item):
        success = self.inventory.add_item(item)
        return success
    
    def drop_item(self, item: Item):
        self.inventory.remove_item(item)

    def add_status(self, status: Status):
            if not status.stackble:
                self.statuses.discard(status)
            self.statuses.add(status)
            if status.on_apply:
                status.on_apply(self)

    def remove_status(self,status_to_remove: Status):
        if status_to_remove in self.statuses:
            self.statuses.discard(status_to_remove)
    
    def remove_status_by_name(self, name: str):
        to_remove = [s for s in self.statuses if s.name == name]

        for status in to_remove:
            self.statuses.discard(status)
            if status.on_remove:
                status.on_remove(self)


    @classmethod
    def generate_character(cls, name: str):
        stats = Statistics.roll_stats(warhmamer_stat_creation_method)
        return cls(name, stats)
    

class WarhammerCharacter(Character):
    def __init__(self, name: str, stats: Statistics, inventory_size: int = INVENTORY_SIZE, max_health: int = MAX_HEALTH):
        super().__init__(name, stats, inventory_size, max_health)
        self.inventory = WarhammerInventory(INVENTORY_SIZE, INVENTORY_WEIGHT_LIMIT)