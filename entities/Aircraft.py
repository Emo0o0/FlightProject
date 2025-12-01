from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.AircraftType import AircraftType


class Aircraft:
    def __init__(
        self,
        id: Optional[int],
        aircraft_type: "AircraftType",
        registration_number: str,
        total_seats: int,
        manufacture_year: int,
    ):
        self.id = id
        self.aircraft_type = aircraft_type
        self.registration_number = registration_number
        self.total_seats = total_seats
        self.manufacture_year = manufacture_year
