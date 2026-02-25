from app.logic.dice.dice import Dice
from enum import Enum, auto
from typing import List
from character import Character
from typing import Protocol

class ItemTag(Enum):
    # weapon tags
    FINESSE = auto()         
    HEAVY = auto()          
    TWO_HANDED = auto()       
    ARMOR_PIERCING = auto()   
    RANGED = auto()           
    FLAMING = auto()          
    FROST = auto()           
    POISONED = auto()        
    SHARP = auto()           
    CRUSHING = auto()       
    
    # armor tags
    LIGHT = auto()           
    HEAVY_ARMOR = auto()      
    MAGIC_RESISTANT = auto() 

    # other tags
    CURSED = auto()       
    BLESSED = auto()        
    CHAOS_INFUSED = auto()    
    

class ConsumableTarget(Protocol):
    pass

class Item:
    def __init__(self,weight: int, monetary_value: int, tags: List[ItemTag]):
        self.weight = weight
        self.monetary_value = monetary_value
        self.tags = tags

    def get_weight(self):
        return self.weight
    
    def get_monetary_value(self):
        return self.weight
    
    def get_tags(self):
        return self.tags
    

class BreakableItem:
    def __init__(self,weight: int, monetary_value: int, tags: List[ItemTag], durability: int):
        self.durability = durability

    def use(self):
        self.durability -= 1


class Weapon(BreakableItem):
    def __init__(self, weight: int, monetary_value: int, tags: List[ItemTag], durability: int, base_damage: int, damage_dice: Dice):
        super().__init__(weight, monetary_value, tags, durability)
        self.base_damage = base_damage
        self.damage_dice = damage_dice

    def attack(self):
        super().use()


class Armor(BreakableItem):
    def __init__(self, weight: int, monetary_value: int, tags: List[ItemTag], durability: int, protection: int):
        super().__init__(weight, monetary_value, tags, durability)
        self.protection = protection

    

class Consumable(BreakableItem):
    def __init__(self, weight: int, monetary_value: int, tags: List[ItemTag], uses: int):
        super().__init__(weight, monetary_value, tags, uses)

    def consume(self,target: ConsumableTarget):
        super().use()

