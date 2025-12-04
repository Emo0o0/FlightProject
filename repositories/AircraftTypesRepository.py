import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.AircraftType import AircraftType
from Flight_Project.repositories.ManufacturersRepository import ManufacturersRepository
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class AircraftTypesRepository(BaseRepository[AircraftType]):
    def __init__(
        self, db: RepositoryManager, manufacturer_repo: ManufacturersRepository
    ):
        super().__init__(db, "aircraft_types")
        self.manufacturer_repo = manufacturer_repo

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS aircraft_types (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    model TEXT NOT NULL,
                    manufacturer_id INTEGER NOT NULL,
                    engine_count INTEGER,
                    engine_type TEXT,          -- 'turbofan', 'turboprop', 'piston'
                    range_km INTEGER,
                    cruise_speed_kmh INTEGER,
                    FOREIGN KEY (manufacturer_id) REFERENCES manufacturers(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )"""
        )

    def _to_entity(self, row: Tuple) -> AircraftType:
        manufacturer = self.manufacturer_repo.fetch_one(row[2])
        return AircraftType(
            id=row[0],
            model=row[1],
            manufacturer=manufacturer,
            engine_count=row[3],
            engine_type=row[4],
            range_km=row[5],
            cruise_speed_kmh=row[6],
        )

    def _to_tuple(self, aircraft_type: AircraftType) -> Tuple[Any, ...]:
        return (
            aircraft_type.model,
            aircraft_type.manufacturer.id,
            aircraft_type.engine_count,
            aircraft_type.engine_type,
            aircraft_type.range_km,
            aircraft_type.cruise_speed_kmh,
        )

    def _get_insert_columns(self) -> List[str]:
        return [
            "model",
            "manufacturer_id",
            "engine_count",
            "engine_type",
            "range_km",
            "cruise_speed_kmh",
        ]
