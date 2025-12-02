import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.City import City
from Flight_Project.repositories.CountriesRepository import CountriesRepository
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class CitiesRepository(BaseRepository[City]):
    def __init__(self, db: RepositoryManager, country_repo: CountriesRepository):
        self.db = db
        self.country_repo = country_repo

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS cities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    country_id INTEGER NOT NULL,
                    FOREIGN KEY (country_id) REFERENCES countries(id)
                        ON UPDATE CASCADE
                        ON DELETE RESTRICT
                )"""
        )

    def _to_entity(self, row: Tuple) -> City:
        country = self.country_repo.fetch_one(row[2])
        return City(
            id=row[0],
            name=row[1],
            country=country,
        )

    def _to_tuple(self, city: City) -> Tuple[Any, ...]:
        return (
            city.id,
            city.name,
            city.country.id,
        )

    def _get_insert_columns(self) -> List[str]:
        return [
            "id",
            "name",
            "country_id",
        ]
