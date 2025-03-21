import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.configuration.splite_monster_factory import SqliteMonsterFactory

class TestSqliteMonsterFactory(unittest.TestCase):

    def setUp(self):
        self._factory = SqliteMonsterFactory()

    def test_create_monsters(self, dungeon):
        self._factory.create_monsters(dungeon)
        class MockSqliteMonsterConfiguration:
            def create_monsters(self, dungeon):
                self.dungeon = dungeon

        class TestSqliteMonsterFactory(unittest.TestCase):

            def setUp(self):
                self._factory = SqliteMonsterFactory()
                self._factory._config = MockSqliteMonsterConfiguration()

            def test_create_monsters(self):
                dungeon = "test_dungeon"
                self._factory.create_monsters(dungeon)
                self.assertEqual(self._factory._config.dungeon, dungeon)

        if __name__ == '__main__':
            unittest.main()