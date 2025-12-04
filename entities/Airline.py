from typing import Optional

from Flight_Project.entities.City import City
from Flight_Project.entities.Country import Country
from Flight_Project.entities.IATACode import IATACode


class Airline:
    def __init__(
        self,
        name: str,
        iata_code: IATACode,
        email: str,
        phone: str,
        country: Country,
        headquarters: City,
        fleet_size: int,
        founded_year: int,
        id: Optional[int] = None,
    ):
        self.id = id
        self.name = name
        self.iata_code = iata_code
        self.email = email
        self.phone = phone
        self.country = country
        self.headquarters = headquarters
        self.fleet_size = fleet_size
        self.founder_year = founded_year
