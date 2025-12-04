import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.Aircraft import Aircraft
from Flight_Project.repositories.AircraftTypesRepository import AircraftTypesRepository
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class AircraftsRepository(BaseRepository[Aircraft]):
    def __init__(
        self, db: RepositoryManager, aircraft_types_repo: AircraftTypesRepository
    ):
        super().__init__(db, "aircrafts")
        self.aircraft_types_repo = aircraft_types_repo

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

    def _to_entity(self, row: Tuple) -> Aircraft:
        aircraft_type = self.aircraft_types_repo.fetch_one(row[1])
        return Aircraft(
            id=row[0],
            aircraft_type=aircraft_type,
            registration_number=row[2],
            total_seats=row[3],
            manufacture_year=row[4],
        )

    def _to_tuple(self, aircraft: Aircraft) -> Tuple[Any, ...]:
        return (
            aircraft.aircraft_type.id,
            aircraft.registration_number,
            aircraft.total_seats,
            aircraft.manufacture_year,
        )

    def _get_insert_columns(self) -> List[str]:
        return [
            "aircraft_type_id",
            "registration_number",
            "total_seats",
            "manufacture_year",
        ]
