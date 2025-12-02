import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.Manufacturer import Manufacturer
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class ManufacturersRepository(BaseRepository[Manufacturer]):
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS manufacturers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL
                )"""
        )

    def _to_entity(self, row: Tuple) -> Manufacturer:
        return Manufacturer(
            id=row[0],
            name=row[1],
        )

    def _to_tuple(self, manufacturer: Manufacturer) -> Tuple[Any, ...]:
        return (manufacturer.name,)

    def _get_insert_columns(self) -> List[str]:
        return [
            "name",
        ]
