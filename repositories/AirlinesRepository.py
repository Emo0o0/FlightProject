import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.Airline import Airline
from Flight_Project.repositories.IATACodesRepository import IATACodesRepository
from Flight_Project.repositories.CitiesRepository import CitiesRepository
from Flight_Project.repositories.CountriesRepository import CountriesRepository
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class AirlinesRepository(BaseRepository[Airline]):
    def __init__(
        self,
        db: RepositoryManager,
        countries_repo: CountriesRepository,
        cities_repo: CitiesRepository,
        iata_codes_repo: IATACodesRepository,
    ):
        super().__init__(db, "airlines")
        self.countries_repo = countries_repo
        self.cities_repo = cities_repo
        self.iata_codes_repo = iata_codes_repo

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS airlines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    iata_code_id INTEGER NOT NULL,
                    email TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    country_id INTEGER NOT NULL,
                    headquarters_city_id INTEGER NOT NULL,
                    fleet_size INTEGER NOT NULL,
                    founded_year INTEGER NOT NULL,
                    FOREIGN KEY (iata_code_id) REFERENCES iata_codes(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (country_id) REFERENCES countries(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (headquarters_city_id) REFERENCES cities(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )"""
        )

    def _to_entity(self, row: Tuple) -> Airline:
        headquarters_city = self.cities_repo.fetch_one(row[6])
        country = self.countries_repo.fetch_one(row[5])
        iata_code = self.iata_codes_repo.fetch_one(row[2])
        return Airline(
            id=row[0],
            name=row[1],
            iata_code=iata_code,
            email=row[3],
            phone=row[4],
            country=country,
            headquarters=headquarters_city,
            fleet_size=row[7],
            founded_year=row[8],
        )

    def _to_tuple(self, airline: Airline) -> Tuple[Any, ...]:
        return (
            airline.name,
            airline.iata_code.id,
            airline.email,
            airline.phone,
            airline.country.id,
            airline.headquarters.id,
            airline.fleet_size,
            airline.founder_year,
        )

    def _get_insert_columns(self) -> List[str]:
        return [
            "name",
            "iata_code_id",
            "email",
            "phone",
            "country_id",
            "headquarters_city_id",
            "fleet_size",
            "founded_year",
        ]
