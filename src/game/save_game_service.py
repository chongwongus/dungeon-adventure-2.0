from src.database.sqlite_dungeon_configuration import SqliteDungeonConfiguration


class SaveGameService:

    def __init__(self):
        self._sqlite_dungeon_configuration = SqliteDungeonConfiguration()

    def save(self, dungeon):
        self._sqlite_dungeon_configuration.save(dungeon)

    def load(self):
        return self._sqlite_dungeon_configuration.load()