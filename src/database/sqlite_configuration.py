import sqlite3

from src.configuration import Configuration

class SqlLiteConfiguration(Configuration):
    def __init__(self, db_name):
        self.db_name = db_name
    
    def __enter__(self):
        self.con = sqlite3.connect(self.db_name)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def close_connection(self):
        self.get_connection().close()