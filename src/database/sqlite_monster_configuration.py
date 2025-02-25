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
        
    def configure(self, dungeon):
        SqlLiteConfiguration.open_db(self)
        cursor = self._con.cursor()
        mosters = []
        cursor.execute("SELECT * FROM monster")
        rows = cursor.fetchall()
        for row in rows:
            for i in range(row[0]):
                monster = self._monster_factory.create_monster(row[1], row[2],row[3], row[4],row[5], row[6], row[7], row[8], row[9])
                mosters.append(monster)
        SqlLiteConfiguration.close_db(self)
        return mosters