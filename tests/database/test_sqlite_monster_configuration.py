import unittest
from unittest.mock import MagicMock, patch

from src.characters.base.monster import Monster
from src.database.sqlite_monster_configuration import SqliteMonsterConfiguration
from src.dungeon.dungeon import Dungeon


class TestSqliteMonsterConfiguration(unittest.TestCase):

    def setUp(self):
        self.monster_configuration = SqliteMonsterConfiguration()

    def test_init_creates_table_and_inserts_monsters(self):
        test_dungeon = Dungeon()
        monsters = self.monster_configuration.configure(test_dungeon)

        self.assertIsNotNone(monsters)
        self.assertLess(0, len(monsters))
        for monster in monsters:
            self.assertIsInstance(monster, Monster)
            self.assertIsNotNone(monster.name)

if __name__ == '__main__':
    unittest.main()