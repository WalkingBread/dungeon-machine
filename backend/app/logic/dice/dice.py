from random import randint

class Dice:
    def __init__(self, sides: int):
        self.sides = sides

    def roll(self):
        return randint(1, self.sides)
    
class D6:
    def __init__(self):
        super().__init__(6)

class D20:
    def __init__(self):
        super().__init__(20)

class D100:
    def __init__(self):
        super().__init__(100)
