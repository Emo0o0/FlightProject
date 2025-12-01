from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from entities.Manufacturer import Manufacturer


class AircraftType:
    def __init__(
        self,
        id: Optional[id],
        model: str,
        manufacturer: "Manufacturer",
        engine_count: int,
        engine_type: str,
        range_km: int,
        cruise_speed_kmh: int,
    ):
        self.id = id
        self.model = model
        self.manufacturer = manufacturer
        self.engine_count = engine_count
        self.engine_type = engine_type
        self.range_km = range_km
        self.cruise_speed_kmh = cruise_speed_kmh
