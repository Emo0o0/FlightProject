from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.Booking import Booking
    from entities.Flight import Flight
    from entities.User import User


class Ticket:
    def __init__(
        self,
        id: Optional[int],
        ticket_number: str,
        booking: "Booking",
        flight: "Flight",
        user: "User",
        seat_number: str,
        ticket_class: str,
        ticket_status: str,
        issued_at: str,
        checked_in_at: str,
        boarded_at: str,
        cancelled_at: str,
        no_show_at: str,
    ):
        self.id = id
        self.ticket_number = ticket_number
        self.booking = booking
        self.flight = flight
        self.user = user
        self.seat_number = seat_number
        self.ticket_class = ticket_class
        self.ticket_status = ticket_status
        self.issued_at = issued_at
        self.checked_in_at = checked_in_at
        self.boarded_at = boarded_at
        self.cancelled_at = cancelled_at
        self.no_show_at = no_show_at
