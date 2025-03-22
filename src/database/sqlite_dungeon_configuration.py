import uuid
from typing import Tuple

from src.characters.base.monster import Monster
from src.characters.heroes.hero_factory import HeroFactory
from src.characters.monsters.monster_factory import MonsterFactory
from src.database.sqlite_configuration import SqliteConfiguration
from src.database.sqlite_hero_configuration import SqliteHeroConfiguration
from src.database.sqlite_table_constants import TableConstants
from src.dungeon.dungeon import Dungeon
from src.dungeon.room import Room
from src.game.game_data import GameData


class SqliteRoomMonster:
    def __init__(self, room_id, monster: Monster):
        self.room_id = room_id
        self.name = monster.name
        self.hp = monster.hp
        self.min_damage = monster._min_damage
        self.max_damage = monster._max_damage
        self.attack_speed = monster._attack_speed
        self.hit_chance = monster._hit_chance
        self.heal_chance = monster.heal_chance
        self.min_heal = monster.min_heal
        self.max_heal = monster.max_heal

class SqliteRoom:
    def __init__(self, position: Tuple[int, int], room: Room):
        self.room_id = str(uuid.uuid4())
        self.x_pos = position[0]
        self.y_pos = position[1]
        self.has_pit = room.hasPit
        self.has_health_pot = room.hasHealthPot
        self.has_vision_pot = room.hasVisionPot
        self.has_pillar = room.hasPillar
        self.pillar_type = room.pillarType
        self.doors = result = ','.join([str(door) for door in room.doors.values()])
        self.is_exit = room.isExit
        self.is_entrance = room.isEntrance
        self.visited = room.visited

class SqliteDungeon:
    def __init__(self, dungeon: Dungeon):
        self.dungeon_id = str(uuid.uuid4())
        self.x_size = dungeon.size[0]
        self.y_size = dungeon.size[1]
        self.entrance_x = dungeon.entrance[0]
        self.entrance_y = dungeon.entrance[1]
        self.exit_x = dungeon.exit[0]
        self.exit_y = dungeon.exit[1]

class SqliteDungeonConfiguration(SqliteConfiguration):
    def __init__(self):
        SqliteConfiguration.__init__(self)
        SqliteConfiguration.open_db(self)

        cursor = self._con.cursor()

        # Create Dungeon
        cursor.execute(f"CREATE TABLE IF NOT EXISTS dungeon ("
                       "dungeon_id TEXT PRIMARY KEY, "
                       "x_size INTEGER, "
                       "y_size INTEGER, "
                       "entrance_x INTEGER, "
                       "entrance_y INTEGER, "
                       "exit_x INTEGER, "
                       "exit_y INTEGER)"
                       )

        # Get Dungeon Rooms
        cursor.execute(f"CREATE TABLE IF NOT EXISTS dungeon_rooms ("
                       "room_id TEXT PRIMARY KEY, "
                       "x_pos INTEGER, "
                       "y_pos INTEGER, "
                       "has_pit BOOLEAN, "
                       "has_health_pot BOOLEAN, "
                       "has_vision_pot BOOLEAN, "
                       "has_pillar BOOLEAN, "
                       "pillar_type BOOLEAN, "
                       "doors TEXT, "
                       "is_exit BOOLEAN, "
                       "is_entrance BOOLEAN, "
                       "visited BOOLEAN)"
                       )

        #Get Dungeon Monster
        cursor.execute(f"CREATE TABLE IF NOT EXISTS dungeon_room_monster ("
                       "room_id TEXT, "
                       "name TEXT, "
                       "hp INTEGER,"
                       "min_damage INTEGER,"
                       "max_damage INTEGER,"
                       "attack_speed INTEGER,"
                       "hit_chance FLOAT,"
                       "heal_chance FLOAT,"
                       "min_heal INTEGER,"
                       "max_heal INTEGER)"
                       )
        SqliteConfiguration.close_db(self)

    def clear_db(self):
        SqliteConfiguration.open_db(self)

        cursor = self._con.cursor()

        cursor.execute(f"DELETE FROM dungeon")
        cursor.execute(f"DELETE FROM dungeon_rooms")
        cursor.execute(f"DELETE FROM dungeon_room_monster")

        self._con.commit()
        SqliteConfiguration.close_db(self)

    def save(self, dungeon: Dungeon):
        self.clear_db()

        SqliteConfiguration.open_db(self)

        cursor = self._con.cursor()

        sqlite_dungeon = SqliteDungeon(dungeon)
        cursor.execute(f"INSERT INTO dungeon VALUES (?, ?, ?, ?, ?, ?, ?)", (
            sqlite_dungeon.dungeon_id,
            sqlite_dungeon.x_size,
            sqlite_dungeon.y_size,
            sqlite_dungeon.entrance_x,
            sqlite_dungeon.entrance_y,
            sqlite_dungeon.exit_x,
            sqlite_dungeon.exit_y))

        for x in range(dungeon.size[0]):
            for y in range(dungeon.size[1]):
                room = dungeon.get_room(x, y)
                sqlite_room = SqliteRoom((x,y),room)
                cursor.execute(f"INSERT INTO dungeon_rooms VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                    sqlite_room.room_id,
                    sqlite_room.x_pos,
                    sqlite_room.y_pos,
                    sqlite_room.has_pit,
                    sqlite_room.has_health_pot,
                    sqlite_room.has_vision_pot,
                    sqlite_room.has_pillar,
                    sqlite_room.pillar_type,
                    sqlite_room.doors,
                    sqlite_room.is_exit,
                    sqlite_room.is_entrance,
                    sqlite_room.visited
                ))
                if room.monster is not None:
                    sqlite_monster = SqliteRoomMonster(sqlite_room.room_id, room.monster)
                    cursor.execute(f"INSERT INTO dungeon_room_monster VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
                        sqlite_monster.room_id,
                        sqlite_monster.name,
                        sqlite_monster.hp,
                        sqlite_monster.min_damage,
                        sqlite_monster.max_damage,
                        sqlite_monster.attack_speed,
                        sqlite_monster.hit_chance,
                        sqlite_monster.heal_chance,
                        sqlite_monster.min_heal,
                        sqlite_monster.max_heal
                    ))
        self._con.commit()
        SqliteConfiguration.close_db(self)

    def load(self):
        print("Loading Dungeon")
        SqliteConfiguration.open_db(self)
        cursor = self._con.cursor()
        sqlite_dungeon = self.load_dungeon(cursor)
        sqlite_rooms = self.load_dungeon_rooms(cursor)

        if sqlite_dungeon is None:
            return False

        dungeon = Dungeon()
        dungeon.size = (sqlite_dungeon[1], sqlite_dungeon[2])
        dungeon.maze = [[Room() for _ in range(dungeon.size[0])] for _ in range(dungeon.size[1])]
        dungeon.entrance = (sqlite_dungeon[3], sqlite_dungeon[4])
        dungeon.exit= (sqlite_dungeon[5], sqlite_dungeon[6])

        for sql_room in sqlite_rooms:
            room = Room()
            room.hasPit = sql_room[3] == 1
            room.hasHealthPot = sql_room[4] == 1
            room.hasVision = sql_room[5] == 1
            room.hasPillar = sql_room[6] == 1
            room.pillarType = sql_room[7]
            has_door = sql_room[8].split(",")
            doors = {
                'N': has_door[0]== "True", 'S': has_door[1]== "True",
                'E': has_door[2]== "True", 'W': has_door[3]== "True"
            }
            room.doors = doors
            room.isExit = sql_room[9] == 1
            room.isEntrance = sql_room[10] == 1
            room.visited = sql_room[11] == 1

            sql_monster = self.load_dungeon_room_monster(cursor, sql_room[0])
            if(sql_monster is not None):
                monster = MonsterFactory.create_monster(
                    sql_monster[1],
                    sql_monster[2],
                    sql_monster[3],
                    sql_monster[4],
                    sql_monster[5],
                    sql_monster[6],
                    sql_monster[7],
                    sql_monster[8],
                    sql_monster[9]
                )
                room.monster = monster

            dungeon.maze[sql_room[2]][sql_room[1]] = room


        print("Loading Hero")

        hero_config = SqliteHeroConfiguration()
        hero = hero_config.load()

        print(hero)

        if hero is None:
            print("No Hero found")
            self.clear_db(cursor)
        SqliteConfiguration.close_db(self)
        return GameData(dungeon, hero)

    def load_dungeon(self, cursor):
        SqliteConfiguration.open_db(self)
        monsters = []
        cursor.execute(f"SELECT * FROM dungeon")
        rows = cursor.fetchall()
        print(rows)
        if len(rows) > 0:
            return rows[0]

    def load_dungeon_rooms(self, cursor):
        cursor.execute(f"SELECT * FROM dungeon_rooms")
        sql_rooms = cursor.fetchall()

        return sql_rooms

    def load_dungeon_room_monster(self, cursor, room_id):
        monsters = []
        cursor.execute("SELECT * FROM dungeon_room_monster WHERE room_id = ?", (room_id,))
        monster = cursor.fetchall()
        if len(monster) == 0:
            return None
        return monster[0]