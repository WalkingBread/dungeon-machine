from app.logic.dice import Dice

class Item:
    def __init__(self):
        pass

class BreakableItem(Item):
    def __init__(self, durability: int):
        self.durability = durability

class Weapon(BreakableItem):
    def __init__(self, durability: int, base_damage: int, damage_dice: Dice):
        super().__init__(durability)
        self.base_damage = base_damage
        self.damage_dice = damage_dice

