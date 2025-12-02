import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.IATACode import IATACode
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class IATACodesRepository(BaseRepository[IATACode]):
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS iata_codes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    code TEXT NOT NULL UNIQUE
                )"""
        )

    def _to_entity(self, row: Tuple) -> IATACode:
        return IATACode(
            id=row[0],
            code=row[1],
        )

    def _to_tuple(self, iata_code: IATACode) -> Tuple[Any, ...]:
        return (
            iata_code.id,
            iata_code.code,
        )

    def _get_insert_columns(self) -> List[str]:
        return [
            "id",
            "code",
        ]
