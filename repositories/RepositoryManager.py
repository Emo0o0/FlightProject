import sqlite3


class RepositoryManager:
    def __init__(self, db_path="flights.sqlite"):
        self.db_path = db_path
        self.conn = None

    def connect(self):
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute("PRAGMA foreign_keys = ON")
        return self.conn

    def cursor(self):
        return self.connect().cursor()

    def execute(self, query, params=()):
        cur = self.cursor()
        cur.execute(query, params)
        self.connect().commit()
        return cur

    def query(self, query, params=()):
        cur = self.cursor()
        cur.execute(query, params)
        return cur

    def initiate_tables(self):
        pass

    def close(self):
        if self.conn:
            self.conn.close()
            self.conn = None
