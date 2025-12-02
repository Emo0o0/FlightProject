import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.Flight import Flight
from Flight_Project.repositories.AircraftsRepository import AircraftsRepository
from Flight_Project.repositories.AirlinesRepository import AirlinesRepository
from Flight_Project.repositories.AirportsRepository import AirportsRepository
from Flight_Project.repositories.BaseRepository import BaseRepository
from Flight_Project.repositories.FlightStatusesRepository import (
    FlightStatusesRepository,
)
from Flight_Project.repositories.RepositoryManager import RepositoryManager


class FlightsRepository(BaseRepository[Flight]):
    def __init__(
        self,
        db: RepositoryManager,
        airlines_repo: AirlinesRepository,
        aircrafts_repo: AircraftsRepository,
        airports_repo: AirportsRepository,
        flights_status_repo: FlightStatusesRepository,
    ):
        self.db = db
        self.airlines_repo = airlines_repo
        self.aircrafts_repo = aircrafts_repo
        self.airports_repo = airports_repo
        self.flights_status_repo = flights_status_repo

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

    # TODO HANDLE M:M
    def _to_entity(self, row: Tuple) -> Flight:
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
            expected_departure_time=row[7],
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

    def _to_tuple(self, flight: Flight) -> Tuple[Any, ...]:
        return (
            flight.id,
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
            "id",
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
