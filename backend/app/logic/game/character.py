from logic.character import Character
from logic.character.stat import Statistics, StatType

class GameCharacter(Character):
    def __init__(self, name: str, stats: Statistics,
                 inventory_size: int, max_health: int):
        super().__init__(name, stats, inventory_size, max_health)

    @property
    def dead(self):
        return self.health == 0


MAX_HEALTH = 15
INVENTORY_SIZE = 10

STAT_UPGRADE_VALUE = 1

class PlayerCharacter(GameCharacter):
    def __init__(self, name: str, stats: Statistics):
        super().__init__(name, stats, INVENTORY_SIZE, MAX_HEALTH)

    def upgrade_stat(self, stat_type: StatType):
        self.stats.upgrade_stat(stat_type, STAT_UPGRADE_VALUE)

class NonPlayableCharacter(GameCharacter):
    def __init__(self, name: str, stats: Statistics):
        super().__init__(name, stats, INVENTORY_SIZE, MAX_HEALTH)