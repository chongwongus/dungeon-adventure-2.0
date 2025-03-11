import uuid
from typing import Tuple

from src.characters.base.monster import Monster
from src.database.sqlite_configuration import SqliteConfiguration
from src.dungeon.dungeon import Dungeon
from src.dungeon.room import Room

class SqliteRoomMonster:
    def __init__(self, room_id, monster: Monster):
        self.room_id = room_id
        self.name: monster.name
        self.hp: monster.hp
        self.min_damage: monster._min_damage
        self.max_damage: monster._max_damage
        self.attack_speed: monster._attack_speed
        self.hit_chance: monster._hit_chance
        self.heal_chance: monster._heal_chance
        self.min_heal: monster._min_heal
        self.max_heal: monster._max_heal

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
        self.doors = room.doors.__str__()
        self.is_exit = room.isExit
        self.is_entrance = room.isEntrance

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

    def save(self, dungeon: Dungeon):
        SqliteConfiguration.__init__(self)
        SqliteConfiguration.open_db(self)

        cursor = self._con.cursor()

        # Create Dungeon
        cursor.execute("CREATE TABLE IF NOT EXISTS dungeon ("
                       "dungeon_id TEXT PRIMARY KEY, "
                       "x_size INTEGER, "
                       "y_size INTEGER, "
                       "entrance_x INTEGER, "
                       "entrance_y INTEGER, "
                       "exit_x INTEGER, "
                       "exit_y INTEGER)"
                       )

        # Get Dungeon Rooms
        cursor.execute("CREATE TABLE IF NOT EXISTS dungeon_room ("
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
                       "is_entrance BOOLEAN)"
                       )

        #Get Dungeon Monster
        cursor.execute("CREATE TABLE IF NOT EXISTS dungeon_room_monster ("
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

        cursor.execute("DELETE FROM dungeon")
        cursor.execute("DELETE FROM dungeon_room")
        cursor.execute("DELETE FROM dungeon_room_monster")

        sqlite_dungeon = SqliteDungeon(dungeon)
        cursor.execute("INSERT INTO dungeon VALUES (?, ?, ?, ?, ?, ?, ?)", sqlite_dungeon)

        for x in range(dungeon.size[0]):
            for y in range(dungeon.size[1]):
                room = dungeon.get_room(x, y)
                sqlite_room = SqliteRoom(room)
                cursor.execute("INSERT INTO dungeon_room VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sqlite_dungeon)
                if room.monster is not None:
                    sqlite_monster = SqliteRoomMonster(sqlite_room.room_id, room.monster)
                    cursor.execute("INSERT INTO dungeon_room_monster VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", sqlite_monster)
