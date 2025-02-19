import sqlite3
from src.configuration import DungeonConfiguration
from src.logging.start_up_logger import log_config_method_call


class SqlLiteConfiguration(DungeonConfiguration):
    def __init__(self, db_name):
        self.db_name = db_name

    @log_config_method_call
    def __enter__(self):
        self.con = sqlite3.connect(self.db_name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def close_connection(self):
        self.get_connection().close()