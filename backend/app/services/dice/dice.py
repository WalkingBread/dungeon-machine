from logic.dice import DiceSet
from logic.dice.type import DiceType

class DiceService:
    def __init__(self):
        self.dice_set = DiceSet()

    def roll_dice(self, dice_type: DiceType) -> int:
        return self.dice_set.get_dice(dice_type).roll()