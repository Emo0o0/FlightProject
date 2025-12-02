import sqlite3
from time import timezone
from typing import Any, List, Tuple

from Flight_Project.entities.Airport import Airport
from Flight_Project.repositories.CitiesRepository import CitiesRepository
from Flight_Project.repositories.CountriesRepository import CountriesRepository
from Flight_Project.repositories.IATACodesRepository import IATACodesRepository
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class AirportsRepository(BaseRepository[Airport]):
    def __init__(
        self,
        db: RepositoryManager,
        iata_codes_repo: IATACodesRepository,
        cities_repo: CitiesRepository,
        countries_repo: CountriesRepository,
    ):
        self.db = db
        self.iata_codes_repo = iata_codes_repo
        self.cities_repo = cities_repo
        self.countries_repo = countries_repo

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS airports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    iata_code_id INTEGER NOT NULL,
                    country_id INTEGER NOT NULL,
                    city_id INTEGER NOT NULL,
                    timezone TEXT NOT NULL,
                    elevation TEXT,
                    FOREIGN KEY (iata_code_id) REFERENCES iata_codes(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (country_id) REFERENCES countries(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (city_id) REFERENCES cities(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )"""
        )

        self.db.execute(
            """CREATE INDEX IF NOT EXISTS idx_airports_iata ON airports(iata_code_id)"""
        )

    def _to_entity(self, row: Tuple) -> Airport:
        iata_code = self.iata_codes_repo.fetch_one(row[2])
        country = self.countries_repo.fetch_one(row[3])
        city = self.countries_repo.fetch_one(row[4])
        return Airport(
            id=row[0],
            name=row[1],
            iata_code=iata_code,
            country=country,
            city=city,
            timezone=row[5],
            elevation=row[6],
        )

    def _to_tuple(self, airport: Airport) -> Tuple[Any, ...]:
        return (
            airport.id,
            airport.name,
            airport.iata_code.id,
            airport.country.id,
            airport.city.id,
            airport.timezone,
            airport.elevation,
        )

    def _get_insert_columns(self) -> List[str]:
        return [
            "id",
            "name",
            "iata_code_id",
            "country_id",
            "city_id",
            "timezone",
            "elevation",
        ]
