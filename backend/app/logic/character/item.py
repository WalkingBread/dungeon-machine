class Item:
    def __init__(self):
        pass

class BreakableItem(Item):
    def __init__(self, durability: int):
        self.durability = durability
