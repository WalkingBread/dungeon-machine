from app.logic.character import Character
from app.logic.character.stat import Statistics, StatType

MAX_HEALTH = 15
INVENTORY_SIZE = 10
STAT_UPGRADE_VALUE = 1

class Player(Character):
    def __init__(self, name: str, stats: Statistics):
        super().__init__(name, stats, INVENTORY_SIZE, MAX_HEALTH)
        
    def upgrade_stat(self, stat_type: StatType):
        self.stats.upgrade_stat(stat_type, STAT_UPGRADE_VALUE)    