import sqlite3

from Flight_Project.entities.Aircraft import Aircraft
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class AircraftsRepository(BaseRepository[Aircraft]):
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS aircrafts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    aircraft_type_id INTEGER NOT NULL,
                    registration_number TEXT NOT NULL UNIQUE,  -- e.g. N12345
                    total_seats INTEGER NOT NULL,
                    manufacture_year INTEGER,
                    FOREIGN KEY (aircraft_type_id) REFERENCES aircraft_types(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )"""
        )
