import sqlite3

from Flight_Project.entities.FlightStatusHistory import FlightStatusHistory
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class FlightsStatusHistoryRepository(BaseRepository[FlightStatusHistory]):
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS flight_status_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flight_id INTEGER NOT NULL,
                    old_status_id INTEGER,
                    new_status_id INTEGER NOT NULL,
                    changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (flight_id) REFERENCES flights(id)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (old_status_id) REFERENCES flight_statuses(id)
                        ON UPDATE CASCADE ON DELETE SET NULL,
                    FOREIGN KEY (new_status_id) REFERENCES flight_statuses(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )"""
        )
