import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.Booking import Booking
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository
from Flight_Project.repositories.UsersRepository import UsersRepository


class BookingsRepository(BaseRepository[Booking]):
    def __init__(self, db: RepositoryManager, users_repo: UsersRepository):
        self.db = db
        self.users_repo = users_repo

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    booking_reference TEXT NOT NULL,
                    user_id INTEGER NOT NULL,
                    number_of_passengers INTEGER NOT NULL,
                    total_amount REAL NOT NULL,
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

    # TODO ADD FLIGHTS TO BOOKING FROM M:M
    def _to_entity(self, row: Tuple) -> Booking:
        user = self.users_repo.fetch_one(row[2])
        return Booking(
            id=row[0],
            booking_reference=row[1],
            user=user,
            number_of_passengers=row[3],
            total_amount=row[4],
            created_at=row[5],
        )

    def _to_tuple(self, booking: Booking) -> Tuple[Any, ...]:
        return (
            booking.id,
            booking.booking_reference,
            booking.user.id,
            booking.number_of_passengers,
            booking.total_amount,
            booking.created_at,
        )

    def _get_insert_columns(self) -> List[str]:
        return [
            "id",
            "booking_reference",
            "user_id",
            "number_of_passengers",
            "total_amount",
            "created_at",
        ]
