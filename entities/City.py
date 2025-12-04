from typing import TYPE_CHECKING, Optional

from Flight_Project.entities.Country import Country

# if TYPE_CHECKING:
# from Flight_Project.entities.Country import Country


class City:
    def __init__(
        self,
        name: str,
        country: Country,
        id: Optional[int] = None,
    ):

        self.name = name
        self.country = country
        self.id = id
