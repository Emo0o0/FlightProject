import sqlite3

from Flight_Project.repositories.RepositoryManager import RepositoryManager


class AirportsRepository:
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS airports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    iata_code_id INTEGER NOT NULL,
                    country_id INTEGER NOT NULL,
                    city_id INTEGER NOT NULL,
                    timezone TEXT NOT NULL,
                    elevation TEXT,
                    FOREIGN KEY (iata_code_id) REFERENCES iata_codes(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (country_id) REFERENCES countries(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (city_id) REFERENCES cities(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )"""
        )

        self.db.execute(
            """CREATE INDEX IF NOT EXISTS idx_airports_iata ON airports(iata_code_id)"""
        )
