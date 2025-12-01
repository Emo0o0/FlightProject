import sqlite3

from Flight_Project.entities.Booking import Booking
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class BookingsRepository(BaseRepository[Booking]):
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                        ON UPDATE CASCADE ON DELETE CASCADE
                )"""
        )

        self.db.execute(
            """CREATE TABLE IF NOT EXISTS bookings_flights (
                    booking_id INTEGER NOT NULL,
                    flight_id INTEGER NOT NULL,
                    PRIMARY KEY (booking_id, flight_id),
                    FOREIGN KEY (booking_id) REFERENCES bookings(id)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (flight_id) REFERENCES flights(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )"""
        )
