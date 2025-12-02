from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.Flight import Flight
    from entities.FlightStatus import FlightStatus


class FlightStatusHistory:
    def __init__(
        self,
        flight: "Flight",
        old_status: "FlightStatus",
        new_status: "FlightStatus",
        changed_at: str,
        notes: str,
        id: Optional[int] = None,
    ):
        self.id = id
        self.flight = flight
        self.old_status = old_status
        self.new_status = new_status
        self.changed_at = changed_at
        self.notes = notes
