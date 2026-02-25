from app.logic.character.item import Item
from app.logic.character.status import Status, INFINITE_DURATION
from typing import Protocol, List


class Inventory:
    def __init__(self, item_limit: int, weight_limit: int):
        self.item_limit = item_limit
        self.weight_limit = weight_limit
        self._inventory = []

    def get_inventory(self):
        return set(self._inventory)
    
    def get_inventory_weight(self):
        return sum(item.get_weight() for item in self._inventory)
    
    def get_inventory_item_number(self):
        return len(self._inventory)

    def add_item(self, item: Item):
        if self.get_inventory_item_number() == self.item_limit and self.get_inventory_weight() + item.get_weight() > self.weight_limit:
            return False
        
        self._inventory.append(item)
        return True
    
    def remove_item(self, item: Item):
        if item in self._inventory:
            self._inventory.remove(item)

    def set_weight_limit(self,weight_limit: int):
        if weight_limit > 0:
            self.weight_limit = weight_limit



class InventoryHolder(Protocol):

    statuses: List[Status]
    def add_status(self, status: Status) -> None:
        ...

    def remove_status(self,status_to_remove: Status) -> None:
        ...
    
    def remove_status_by_name(self,status_to_remove_name: str) -> None:
        ...
    

    
class WarhammerInventory(Inventory):

    def __init__(self, item_limit: int, weight_limit: int):
        super().__init__(item_limit, weight_limit)


    @classmethod
    def calculate_weight_limit(cls,strength:int ,toughness: int):
        return 5*(strength + toughness)


    def add_item(self, item: Item, inventory_owner: InventoryHolder ):
        if self.get_inventory_item_number() == self.item_limit:
            return False
        self._inventory.append(item)
        if self.get_inventory_weight() > self.weight_limit:
            inventory_owner.add_status(Status("Encumbered",INFINITE_DURATION,False))
        return True
    
    def remove_item(self, item: Item, inventory_owner: InventoryHolder ):
        if not item in self._inventory:
            return False
        self._inventory.remove(item)
        if self.get_inventory_weight() <= self.weight_limit:
            inventory_owner.remove_status_by_name("Encumbered")
        return True
    


