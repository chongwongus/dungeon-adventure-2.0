from src.database.sqlite_configuration import SqliteConfiguration

class SqliteGameSave:

    def __init__(self):
        print("Game Save")

class SqliteSaveGameConfiguration(SqliteConfiguration):

    def __init__(self):
        super().__init__()
        _table_name = "game_configuration"

    def save(self, gameSave: SqliteGameSave):
        SqliteConfiguration.open_db(self)

        cursor = self._con.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS ${self._table_name} (state INTEGER,)")
        cursor.execute("DELETE FROM ${self._table_name}")

        cursor.execute("INSERT INTO ${self._table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", gameSave)