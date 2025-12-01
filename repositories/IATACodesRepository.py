import sqlite3

from Flight_Project.entities.IATACode import IATACode
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class IATACodesRepository(BaseRepository[IATACode]):
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS iata_codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT NOT NULL UNIQUE
                )"""
        )
