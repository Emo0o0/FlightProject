from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.Airline import Airline
    from entities.Aircraft import Aircraft
    from entities.Airport import Airport
    from entities.FlightStatus import FlightStatus
    from entities.Booking import Booking


class Flight:
    def __init__(
        self,
        id: Optional[int],
        flight_number: str,
        airline: "Airline",
        aircraft: "Aircraft",
        origin_airport: "Airport",
        destination_airport: "Airport",
        expected_departure_time,
        expected_arrival_time,
        actual_departure_time,
        actual_arrival_time,
        total_seats: int,
        available_seats: int,
        seat_price: float,
        flight_status: "FlightStatus",
        departure_gate: str,
        departure_terminal: str,
        arrival_gate: str,
        arrival_terminal: str,
    ):
        self.id = id
        self.flight_number = flight_number
        self.airline = airline
        self.aircraft = aircraft
        self.origin_airport = origin_airport
        self.destination_airport = destination_airport
        self.expected_departure_time = expected_departure_time
        self.expected_arrival_time = expected_arrival_time
        self.actual_departure_time = actual_departure_time
        self.actual_arrival_time = actual_arrival_time
        self.total_seats = total_seats
        self.available_seats = available_seats
        self.seat_price = seat_price
        self.flight_status = flight_status
        self.departure_gate = departure_gate
        self.departure_terminal = departure_terminal
        self.arrival_gate = arrival_gate
        self.arrival_terminal = arrival_terminal
        self.bookings: list["Booking"] = []

    def add_booking(self, booking: "Booking"):
        if booking not in self.bookings:
            self.bookings.append(booking)
