import sqlite3
from pathlib import Path


class Database:
    def __init__(self, db_path: Path | str = ":memory:"):
        self._db_path = str(db_path)
        self.conn = sqlite3.connect(
            str(self._db_path), check_same_thread=False
        )
        print(f"connected to {self._db_path}")
        self.ensure_migrations()

    def ensure_migrations(self):
        create_games_table_sql = r"""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY
          , data TEXT NOT NULL
        )
        """
        cursor = self.conn.cursor()
        cursor.execute(create_games_table_sql)
        cursor.close()
