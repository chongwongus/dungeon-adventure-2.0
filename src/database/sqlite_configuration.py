import sqlite3

from src.configuration.dungeon_configuration import DungeonConfiguration

class SqliteConfiguration(DungeonConfiguration):
    def __init__(self, db_name):
        self.db_name = db_name
        self._con = None

    def open_db(self):
        self._con = sqlite3.connect(self.db_name)

    def close_db(self):
        self._con.close()
