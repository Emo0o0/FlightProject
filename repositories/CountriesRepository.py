import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.Country import Country
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class CountriesRepository(BaseRepository[Country]):
    def __init__(self, db: RepositoryManager):
        super().__init__(db, "countries")

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS countries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    country_code TEXT UNIQUE NOT NULL
                )"""
        )

    def get_by_name(self, name: str) -> Country:
        row = self.db.execute(
            """
            SELECT *
            FROM countries
            WHERE name = ?
            """,
            (name,),
        ).fetchone()
        return self._to_entity(row)

    def _to_entity(self, row: Tuple) -> Country:
        return Country(
            id=row[0],
            name=row[1],
            country_code=row[2],
        )

    def _to_tuple(self, country: Country) -> Tuple[Any, ...]:
        return (
            country.name,
            country.country_code,
        )

    def _get_insert_columns(self) -> List[str]:
        return [
            "name",
            "country_code",
        ]
