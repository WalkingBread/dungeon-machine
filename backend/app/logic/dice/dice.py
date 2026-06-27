from random import randint
from logic.dice.type import DiceType

class DiceSet:
    def __init__(self):
        self._dice_set = {
            DiceType.D4: D4(),
            DiceType.D6: D6(),
            DiceType.D10: D10(),
            DiceType.D20: D20(),
            DiceType.D100: D100()
        }

    def get_dice(self, type: DiceType) -> Dice:
        return self._dice_set.get(type)
    

class Dice:
    def __init__(self, sides: int):
        self.sides = sides

    def roll(self):
        return randint(1, self.sides)
    
    def normalize_value(self, value: int):
        return max(1, min(value, self.sides))
    
    
class D4(Dice):
    def __init__(self):
        super().__init__(4)
    
class D6(Dice):
    def __init__(self):
        super().__init__(6)

class D8(Dice):
    def __init__(self):
        super().__init__(8)

class D10(Dice):
    def __init__(self):
        super().__init__(10)

class D20(Dice):
    def __init__(self):
        super().__init__(20)

class D100(Dice):
    def __init__(self):
        super().__init__(100)
