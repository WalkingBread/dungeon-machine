from app.logic.character.inventory import Inventory
from app.logic.character.stat import Statistics

INVENTORY_SIZE = 10

class Character:
    def __init__(self, name: str, stats: Statistics, 
                 inventory_size: int = INVENTORY_SIZE):
        self.name = name
        self.stats = stats
        self.inventory = Inventory(inventory_size)