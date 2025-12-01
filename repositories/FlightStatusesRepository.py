import sqlite3

from Flight_Project.entities.FlightStatus import FlightStatus
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class FlightStatusesRepository(BaseRepository[FlightStatus]):
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS flight_statuses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status TEXT NOT NULL UNIQUE
                )"""
        )
