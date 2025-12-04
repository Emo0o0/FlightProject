import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.FlightStatus import FlightStatus
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class FlightStatusesRepository(BaseRepository[FlightStatus]):
    def __init__(self, db: RepositoryManager):
        super().__init__(db, "flight_statuses")

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS flight_statuses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status TEXT NOT NULL UNIQUE
                )"""
        )

    def _to_entity(self, row: Tuple) -> FlightStatus:
        return FlightStatus(
            id=row[0],
            status=row[1],
        )

    def _to_tuple(self, flight_status: FlightStatus) -> Tuple[Any, ...]:
        return (flight_status.status,)

    def _get_insert_columns(self) -> List[str]:
        return [
            "status",
        ]
