from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.Flight import Flight
    from entities.FlightStatus import FlightStatus


class FlightStatusHistory:
    def __init__(
        self,
        id: Optional[int],
        flight: "Flight",
        old_status: "FlightStatus",
        new_status: "FlightStatus",
        changed_at: str,
        notes: str,
    ):
        pass
