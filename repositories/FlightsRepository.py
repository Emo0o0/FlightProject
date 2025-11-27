import sqlite3

from Flight_Project.repositories.RepositoryManager import RepositoryManager


class FlightsRepository:
    def __init__(self, db: RepositoryManager):
        self.db = db

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
