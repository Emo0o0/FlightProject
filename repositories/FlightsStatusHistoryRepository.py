import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.FlightStatusHistory import FlightStatusHistory
from Flight_Project.repositories.FlightStatusesRepository import (
    FlightStatusesRepository,
)
from Flight_Project.repositories.FlightsRepository import FlightsRepository
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class FlightsStatusHistoryRepository(BaseRepository[FlightStatusHistory]):
    def __init__(
        self,
        db: RepositoryManager,
        flights_repo: FlightsRepository,
        flights_status_repo: FlightStatusesRepository,
    ):
        super().__init__(db, "flight_status_history")
        self.db = db
        self.flights_repo = flights_repo
        self.flights_status_repo = flights_status_repo

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

    def _to_entity(self, row: Tuple) -> FlightStatusHistory:
        flight = self.flights_repo.fetch_one(row[1])
        old_status = (self.flights_status_repo(row[2]),)
        new_status = self.flights_status_repo(row[3])
        return FlightStatusHistory(
            id=row[0],
            flight=flight,
            old_status=old_status,
            new_status=new_status,
            changed_at=row[4],
            notes=row[5],
        )

    def _to_tuple(self, flight_status_history: FlightStatusHistory) -> Tuple[Any, ...]:
        return (
            flight_status_history.flight.id,
            flight_status_history.old_status.id,
            flight_status_history.new_status.id,
            flight_status_history.changed_at,
            flight_status_history.notes,
        )

    def _get_insert_columns(self) -> List[str]:
        return [
            "flight_id",
            "old_status_id",
            "new_status_id",
            "changed_at",
            "notes",
        ]
