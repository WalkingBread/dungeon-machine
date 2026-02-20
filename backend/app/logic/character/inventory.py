from app.logic.character.item import Item

class Inventory:
    def __init__(self, size: int):
        self._max_size = size
        self._inventory = []

    def get_inventory(self):
        return set(self._inventory)
    
    def get_inventory_size(self):
        return len(self._inventory)

    def add_item(self, item: Item):
        if self.get_inventory_size() == self._max_size:
            return False
        
        self._inventory.append(item)
        return True
    
    def remove_item(self, item: Item):
        if item in self._inventory:
            self._inventory.remove(item)