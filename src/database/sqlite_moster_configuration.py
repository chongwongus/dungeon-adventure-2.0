from src.configuration.monster_configuration import MonsterConfiguration
from src.database.sqlite_configuration import SqlLiteConfiguration


class SqliteMonsterConfiguration(MonsterConfiguration, SqlLiteConfiguration):
    
    monsters = [
        (10, "Goblin", 10, 10, 10, 0.8, 0.2, 5, 5),
        (5, "Orc", 20, 20, 20, 0.8, 0.2, 10, 10),
        (3, "Troll", 30, 30, 30, 0.8, 0.2, 15, 15),
        (1, "Dragon", 40, 40, 40, 0.8, 0.2, 20, 20)
    ]
    
    def __init__(self, db_name):
        SqlLiteConfiguration.__init__(self, db_name)
        with self.con as con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS monster (amount INTEGER, name TEXT, hp INTEGER, min_damage INTEGER, max_damage INTEGER, attack_speed INTEGER, hit_chance REAL, heal_chance REAL, min_heal INTEGER, max_heal INTEGER)")
            cur.execute("DELETE FROM monster")
            for monster in self.monsters:
                cur.execute("INSERT INTO monster VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", monster)
            con.commit()
        
    def configure(self, dungeon):
        with self.con as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM monster")
            rows = cur.fetchall()
            for row in rows:
                for i in range(row[0]):
                    monster = {
                        "name": row[1],
                        "hp": row[2],
                        "min_damage": row[3],
                        "max_damage": row[4],
                        "attack_speed": row[5],
                        "hit_chance": row[6],
                        "heal_chance": row[7],
                        "min_heal": row[8],
                        "max_heal": row[9]
                    }
                    dungeon.add_monster(monster)
                
        return dungeon