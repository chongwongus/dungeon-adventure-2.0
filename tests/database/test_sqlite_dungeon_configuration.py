import unittest
from src.database.sqlite_dungeon_configuration import SqliteDungeonConfiguration, SqliteRoom, SqliteRoomMonster, SqliteDungeon
from src.dungeon.easy_factory import EasyDungeonFactory

class TestSqliteDungeonConfiguration(unittest.TestCase):

    def setUp(self):
        self.config = SqliteDungeonConfiguration()
        factory = EasyDungeonFactory()
        self.dungeon = factory.create()

    def test_save_creates_tables_and_inserts_data(self):
        self.config.save(self.dungeon)
        game_data = self.config.load()
        self.assertIsNotNone(game_data.dungeon)
        self.assertEqual(self.dungeon.size, game_data.dungeon.size)
        self.assertEqual(self.dungeon.entrance, game_data.dungeon.entrance)
        self.assertEqual(self.dungeon.exit, game_data.dungeon.exit)

        self.assertEqual(len(self.dungeon.maze), len(game_data.dungeon.maze))

        for x in range(self.dungeon.size[0]):
            for y in range(self.dungeon.size[1]):
                inital_room = self.dungeon.get_room(x,y)
                retrieved_room = game_data.dungeon.get_room(x,y)
                self.assertEqual(inital_room.hasPit, retrieved_room.hasPit)
                self.assertEqual(inital_room.hasPillar, retrieved_room.hasPillar)
                self.assertEqual(inital_room.isExit, retrieved_room.isExit)
                self.assertEqual(inital_room.isEntrance, retrieved_room.isEntrance)
                self.assertEqual(inital_room.pillarType, retrieved_room.pillarType)
                if(inital_room.monster is not None):
                    self.assertIsNotNone(retrieved_room.monster)
                    self.assertEqual(inital_room.monster.name, retrieved_room.monster.name)
                    self.assertEqual(inital_room.monster.hp, retrieved_room.monster.hp)
                    self.assertEqual(inital_room.monster.hp, retrieved_room.monster.hp)


if __name__ == '__main__':
    unittest.main()