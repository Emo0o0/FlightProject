from typing import Optional

from Flight_Project.entities import City, Country, IATACode


class Airport:
    def __init__(
        self,
        name: str,
        iata_code: IATACode,
        country: Country,
        city: City,
        timezone: str,
        elevation: str,
        id: Optional[int] = None,
    ):
        self.id = id
        self.name = name
        self.iata_code = iata_code
        self.country = country
        self.city = city
        self.timezone = timezone
        self.elevation = elevation
