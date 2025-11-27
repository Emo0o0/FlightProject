import sqlite3

from Flight_Project.repositories.RepositoryManager import RepositoryManager


class AirlinesRepository:
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS airlines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    iata_code_id INTEGER NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    country_id INTEGER NOT NULL,
                    headquarters_city_id INTEGER NOT NULL,
                    fleet_size INTEGER NOT NULL,
                    founded_year INTEGER NOT NULL,
                    FOREIGN KEY (iata_code_id) REFERENCES iata_codes(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (country_id) REFERENCES countries(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (headquarters_city_id) REFERENCES cities(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )"""
        )
