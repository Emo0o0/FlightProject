from typing import TYPE_CHECKING, Optional, List


if TYPE_CHECKING:
    from entities.User import User
    from entities.Flight import Flight


class Booking:
    def __init__(
        self,
        id: Optional[int],
        user: "User",
        created_at: str,
        flights: Optional[List["Flight"]] = None,
    ):
        self.id = id
        self.user = user
        self.created_at = created_at
        self.flights = flights or []

    def add_flight(self, flight: "Flight"):
        if flight not in self.flights:
            self.flights.append(flight)
            flight.add_booking(self)
