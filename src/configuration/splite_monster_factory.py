from src.characters.monsters.monster_factory import MonsterFactory
from src.database.sqlite_monster_configuration import SqliteMonsterConfiguration

class SqliteMonsterFactory(MonsterFactory):

    def __init__(self):
        self._config = SqliteMonsterConfiguration()

    def create_monsters(self, dungeon):
        self._config.create_monsters(dungeon)
