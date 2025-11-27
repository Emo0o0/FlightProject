import sqlite3

from Flight_Project.repositories.RepositoryManager import RepositoryManager


class AircraftTypesRepository:
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS aircraft_types (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model TEXT NOT NULL,
                    manufacturer_id INTEGER NOT NULL,
                    engine_count INTEGER,
                    engine_type TEXT,          -- e.g. 'turbofan', 'turboprop', 'piston'
                    range_km INTEGER,
                    cruise_speed_kmh INTEGER,
                    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )"""
        )
