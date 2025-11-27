import sqlite3

from Flight_Project.repositories.RepositoryManager import RepositoryManager


class ManufacturersRepository:
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS manufacturers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )"""
        )
