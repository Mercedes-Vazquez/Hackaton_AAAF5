import sqlite3


class SqliteBasedRepository:
    def __init__(self, config, conn=None):
        self.config = config
        self.conn = conn

    def _connect(self, database):
        if isinstance(database, sqlite3.Connection):
            return database
        else:
            return sqlite3.connect(database)

    def _conn(self):
        if self.conn is not None:
            conn = self.conn
        else:
            conn = self._connect(self.config["database"])

        conn.row_factory = sqlite3.Row
        return conn
