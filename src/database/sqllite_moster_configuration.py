from src.configuration.monster_configuration import MonsterConfiguration
from src.database.sqlite_configuration import SqlLiteConfiguration


class SqlLiteMonsterConfiguration(MonsterConfiguration, SqlLiteConfiguration):
    
    def __init__(self, db_name):
        SqlLiteConfiguration.__init__(self, db_name)
        
    def configure(self):
        pass