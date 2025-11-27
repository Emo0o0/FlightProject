import sqlite3

from Flight_Project.repositories.RepositoryManager import RepositoryManager


class CountriesRepository:
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS countries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    country_code TEXT NOT NULL
                )"""
        )
