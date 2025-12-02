import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.Amenity import Amenity
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class AmenitiesRepository(BaseRepository[Amenity]):
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS amenities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )"""
        )

    def _to_entity(self, row: Tuple) -> Amenity:
        return Amenity(
            id=row[0],
            name=row[1],
        )

    def _to_tuple(self, amenity: Amenity) -> Tuple[Any, ...]:
        return (
            amenity.id,
            amenity.name,
        )

    def _get_insert_columns(self) -> List[str]:
        return [
            "id",
            "name",
        ]
