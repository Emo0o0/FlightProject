import sqlite3

from Flight_Project.entities.City import City
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class CitiesRepository(BaseRepository[City]):
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS cities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    country_id INTEGER NOT NULL,
                    FOREIGN KEY (country_id) REFERENCES countries(id)
                        ON UPDATE CASCADE
                        ON DELETE RESTRICT
                )"""
        )
