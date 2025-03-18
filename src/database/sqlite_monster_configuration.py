import random

from pygame.cursors import Cursor

from src.configuration.monster_configuration import MonsterConfiguration
from src.characters.monsters.monster_factory import MonsterFactory
from src.database.sqlite_configuration import SqliteConfiguration


class SqliteMonsterConfiguration(MonsterConfiguration, SqliteConfiguration):
    
    monsters = [
        (10, "Gremlin", 10, 10, 10, 0.8, 0.2, 5, 5, 1),
        (5, "Ogre", 20, 20, 20, 0.8, 0.2, 10, 10, 2),
        (3, "Skeleton", 30, 30, 30, 0.8, 0.2, 15, 15, 3),
        (1, "Dragon", 40, 40, 40, 0.8, 0.2, 20, 20, 5)
    ]
    
    def __init__(self):
        SqliteConfiguration.__init__(self)
        SqliteConfiguration.open_db(self)

        self._monster_factory = MonsterFactory()

        cursor = self._con.cursor()
        
        cursor.execute("CREATE TABLE IF NOT EXISTS monster (amount INTEGER, name TEXT, hp INTEGER, min_damage INTEGER, max_damage INTEGER, attack_speed INTEGER, hit_chance REAL, heal_chance REAL, max_heal INTEGER, min_heal INTEGER)")
        cursor.execute("SELECT * FROM monster")
        rows = cursor.fetchall()
        if len(rows) == 0:
            self.populate_default_monsters(cursor)

        self._con.commit()
        SqliteConfiguration.close_db(self)

    def populate_default_monsters(self, cursor):
        for monster in self.monsters:
            cursor.execute("INSERT INTO monster VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", monster)


    def _create_monsters(self):
        SqliteConfiguration.open_db(self)
        cursor = self._con.cursor()
        monsters = []
        cursor.execute("SELECT * FROM monster")
        rows = cursor.fetchall()
        for row in rows:
            for i in range(row[0]):
                monster = self._monster_factory.create_monster(row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9])
                monsters.append(monster)
        SqliteConfiguration.close_db(self)
        return monsters
        
    def configure(self, dungeon):
        monsters = self._create_monsters()
        placed_monsters = []
        count_monster_to_place = min(len(monsters), dungeon.size[0]*dungeon.size[1])
        monster = monsters.pop()
        while count_monster_to_place > 0:
            for i in range(dungeon.size[0]):
                for j in range(dungeon.size[1]):
                    room = dungeon.get_room(i, j)
                    if room.monster is None and random.random() < 0.3:
                        room.place_monster(monster)
                        placed_monsters.append(monster)
                        if len(monsters) > 0 :
                            monster = monsters.pop()
                        count_monster_to_place -= 1
        return placed_monsters