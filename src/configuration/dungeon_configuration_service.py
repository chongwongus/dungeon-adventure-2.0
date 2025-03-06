from src.configuration.monster_configuration import MonsterConfiguration
from src.database.sqlite_monster_configuration import SqliteMonsterConfiguration

class DungeonConfigurationService:
    def __init__(self, dungeon_monster_configuration: MonsterConfiguration):
        self.dungeon_monster_configuration = dungeon_monster_configuration

    def configure_monsters(self, dungeon):
        self.dungeon_monster_configuration.configure(dungeon)