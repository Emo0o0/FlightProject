import sqlite3

from Flight_Project.entities.Amenity import Amenity
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class AmenitiesRepository(BaseRepository[Amenity]):
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS amenities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )"""
        )
