import random

from src.configuration.monster_configuration import MonsterConfiguration
from src.characters.monsters.monster_factory import MonsterFactory
from src.database.sqlite_configuration import SqlLiteConfiguration


class SqliteMonsterConfiguration(MonsterConfiguration, SqlLiteConfiguration):
    
    monsters = [
        (10, "Goblin", 10, 10, 10, 0.8, 0.2, 5, 5, 1),
        (5, "Orc", 20, 20, 20, 0.8, 0.2, 10, 10, 2),
        (3, "Troll", 30, 30, 30, 0.8, 0.2, 15, 15, 3),
        (1, "Dragon", 40, 40, 40, 0.8, 0.2, 20, 20, 5)
    ]
    
    def __init__(self):
        SqlLiteConfiguration.__init__(self, "monster")
        SqlLiteConfiguration.open_db(self)

        self._monster_factory = MonsterFactory()

        cursor = self._con.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS monster (amount INTEGER, name TEXT, hp INTEGER, min_damage INTEGER, max_damage INTEGER, attack_speed INTEGER, hit_chance REAL, heal_chance REAL, max_heal INTEGER)")
        cursor.execute("DELETE FROM monster")
        for monster in self.monsters:
            cursor.execute("INSERT INTO monster VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", monster)
        self._con.commit()
        SqlLiteConfiguration.close_db(self)

    def _create_monsters(self):
        SqlLiteConfiguration.open_db(self)
        cursor = self._con.cursor()
        mosters = []
        cursor.execute("SELECT * FROM monster")
        rows = cursor.fetchall()
        for row in rows:
            for i in range(row[0]):
                monster = self._monster_factory.create_monster(row[1], row[2], row[3], row[4], row[5], row[6], row[7],
                                                               row[8], row[9])
                mosters.append(monster)
        SqlLiteConfiguration.close_db(self)
        return mosters
        
    def configure(self, dungeon):
        monsters = self._create_monsters()
        while len(monsters) > 0:
            monster = monsters.pop()
            for i in range(dungeon.size[0]):
                for j in range(dungeon.size[1]):
                    room = dungeon.get_room(i, j)
                    if room.monster is not None and random.random() < 0.3:
                        room.add_monster(monster)
