from __future__ import annotations
import sqlite3
from typing import TYPE_CHECKING, Any, List, Optional, Tuple

from Flight_Project.repositories.BaseRepository import BaseRepository

if TYPE_CHECKING:
    from Flight_Project.entities.Flight import Flight
    from Flight_Project.repositories.AircraftsRepository import AircraftsRepository
    from Flight_Project.repositories.AirlinesRepository import AirlinesRepository
    from Flight_Project.repositories.AirportsRepository import AirportsRepository
    from Flight_Project.repositories.BookingsRepository import BookingsRepository
    from Flight_Project.repositories.FlightStatusesRepository import (
        FlightStatusesRepository,
    )
    from Flight_Project.repositories.RepositoryManager import RepositoryManager
    from Flight_Project.repositories.AmenitiesRepository import AmenitiesRepository


class FlightsRepository(BaseRepository["Flight"]):
    def __init__(
        self,
        db: "RepositoryManager",
        airlines_repo: "AirlinesRepository",
        aircrafts_repo: "AircraftsRepository",
        airports_repo: "AirportsRepository",
        flights_status_repo: "FlightStatusesRepository",
        amenities_repo: "AmenitiesRepository",
        bookings_repo: Optional["BookingsRepository"] = None,
    ):
        super().__init__(db, "flights")
        self.airlines_repo = airlines_repo
        self.aircrafts_repo = aircrafts_repo
        self.airports_repo = airports_repo
        self.flights_status_repo = flights_status_repo
        self.amenities_repo = amenities_repo
        self.bookings_repo = bookings_repo

    def set_bookings_repo(self, bookings_repo: "BookingsRepository") -> None:
        self.bookings_repo = bookings_repo

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS flights (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    flight_number TEXT NOT NULL,
                    airline_id INTEGER NOT NULL,
                    aircraft_id INTEGER NOT NULL,
                    origin_airport_id INTEGER NOT NULL,
                    destination_airport_id INTEGER NOT NULL,
                    expected_departure_time TIMESTAMP NOT NULL,
                    expected_arrival_time TIMESTAMP NOT NULL,
                    actual_departure_time TIMESTAMP,   -- NULL until departed
                    actual_arrival_time TIMESTAMP,     -- NULL until arrived
                    total_seats INTEGER NOT NULL,
                    available_seats INTEGER NOT NULL,
                    seat_price REAL NOT NULL,
                    flight_status_id INTEGER NOT NULL,
                    departure_gate TEXT,
                    departure_terminal TEXT,
                    arrival_gate TEXT,
                    arrival_terminal TEXT,
                    FOREIGN KEY (airline_id) REFERENCES airlines(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (aircraft_id) REFERENCES aircrafts(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (origin_airport_id) REFERENCES airports(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (destination_airport_id) REFERENCES airports(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (flight_status_id) REFERENCES flight_statuses(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )"""
        )

        self.db.execute(
            """CREATE INDEX IF NOT EXISTS idx_flights_flight_number ON flights(flight_number)"""
        )

        self.db.execute(
            """CREATE TABLE IF NOT EXISTS flight_amenities (
                    flight_id INTEGER NOT NULL,
                    amenity_id INTEGER NOT NULL,
                    PRIMARY KEY (flight_id, amenity_id),
                    FOREIGN KEY (flight_id) REFERENCES flights(id)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )"""
        )

    def fetch_user_flights(self, user_id: int) -> List["Flight"]:
        rows = self.db.query(
            """
            SELECT f.*
            FROM bookings b
            JOIN bookings_flights bf ON b.id = bf.booking_id
            JOIN flights f ON bf.flight_id = f.id
            WHERE b.user_id = ?
            ORDER BY f.expected_departure_time DESC
            """,
            (user_id,),
        ).fetchall()
        return [self._to_entity(row) for row in rows]

    def fetch_bookings_for_flight(self, flight_id: int):
        rows = self.db.query(
            """SELECT b.*
                FROM bookings b
                JOIN bookings_flights bf ON bf.booking_id = b.id
                WHERE bf.flight_id = ?""",
            (flight_id,),
        ).fetchall()
        return [self.bookings_repo._to_entity(row) for row in rows]

    def fetch_amenities_for_flight(self, flight_id: int):
        rows = self.db.query(
            """
            SELECT a.*
            FROM amenities a
            JOIN flight_amenities fa ON fa.amenity_id = a.id
            WHERE bf.flight_id = ?
            """,
            (flight_id,),
        ).fetchall()
        return [self.amenities_repo._to_entity(row) for row in rows]

    def fetch_flights_from_to(
        self, city_from, city_to, passenger_count, departure_date
    ):
        rows = self.db.query(
            """
            SELECT f.*
            FROM flights f
            JOIN airports origin_airport ON origin_airport.id = f.origin_airport_id
            JOIN cities origin_city ON origin_city.id = origin_airport.city_id
            JOIN airports dest_airport ON dest_airport.id = f.destination_airport_id
            JOIN cities dest_city ON dest_city.id = dest_airport.city_id
            WHERE origin_city.name = ? AND dest_city.name = ? AND f.available_seats >= ? AND DATE(f.expected_departure_time) >= ?
            """,
            (city_from, city_to, passenger_count, departure_date),
        ).fetchall()
        return [self._to_entity(row) for row in rows]

    def get_flight_by_flight_number(self, flight_number) -> Flight:
        row = self.db.query(
            """
            SELECT *
            FROM flights f
            WHERE f.flight_number = ?
            """,
            (flight_number,),
        ).fetchone()
        return self._to_entity(row)

    def save(self, flight: "Flight") -> "Flight":
        super().save(flight)
        for amenity in flight.amenities:
            self.db.execute(
                """
                INSERT INTO flight_amenities (flight_id, amenity_id) VALUES (?,?)
                """,
                (flight.id, amenity.id),
            )
        return flight

    def _to_entity(self, row: Tuple) -> "Flight":
        from Flight_Project.entities.Flight import Flight

        airline = self.airlines_repo.fetch_one(row[2])
        aircraft = self.aircrafts_repo.fetch_one(row[3])
        origin_airport = self.airports_repo.fetch_one(row[4])
        destination_airport = self.airports_repo.fetch_one(row[5])
        flight_status = self.flights_status_repo.fetch_one(row[13])
        return Flight(
            id=row[0],
            flight_number=row[1],
            airline=airline,
            aircraft=aircraft,
            origin_airport=origin_airport,
            destination_airport=destination_airport,
            expected_departure_time=row[6],
            expected_arrival_time=row[7],
            actual_departure_time=row[8],
            actual_arrival_time=row[9],
            total_seats=row[10],
            available_seats=row[11],
            seat_price=row[12],
            flight_status=flight_status,
            departure_gate=row[13],
            departure_terminal=row[14],
            arrival_gate=row[15],
            arrival_terminal=row[16],
        )

    def _to_tuple(self, flight: "Flight") -> Tuple[Any, ...]:
        return (
            flight.flight_number,
            flight.airline.id,
            flight.aircraft.id,
            flight.origin_airport.id,
            flight.destination_airport.id,
            flight.expected_departure_time,
            flight.expected_arrival_time,
            flight.actual_departure_time,
            flight.actual_arrival_time,
            flight.total_seats,
            flight.available_seats,
            flight.seat_price,
            flight.flight_status.id,
            flight.departure_gate,
            flight.departure_terminal,
            flight.arrival_gate,
            flight.arrival_terminal,
        )

    def _get_insert_columns(self) -> List[str]:
        return [
            "flight_number",
            "airline_id",
            "aircraft_id",
            "origin_airport_id",
            "destination_airport_id",
            "expected_departure_time",
            "expected_arrival_time",
            "actual_departure_time",
            "actual_arrival_time",
            "total_seats",
            "available_seats",
            "seat_price",
            "flight_status_id",
            "departure_gate",
            "departure_terminal",
            "arrival_gate",
            "arrival_terminal",
        ]
