import sqlite3
from typing import TYPE_CHECKING, Any, List, Optional, Tuple

from Flight_Project.repositories.BaseRepository import BaseRepository

if TYPE_CHECKING:
    from Flight_Project.entities.Booking import Booking
    from Flight_Project.repositories.FlightsRepository import FlightsRepository
    from Flight_Project.repositories.RepositoryManager import RepositoryManager
    from Flight_Project.repositories.UsersRepository import UsersRepository


class BookingsRepository(BaseRepository["Booking"]):
    def __init__(
        self,
        db: "RepositoryManager",
        users_repo: "UsersRepository",
        flights_repo: Optional["FlightsRepository"] = None,
    ):
        super().__init__(db, "bookings")
        self.users_repo = users_repo
        self.flights_repo = flights_repo

    def set_flights_repo(self, flights_repo: "FlightsRepository") -> None:
        self.flights_repo = flights_repo

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

    def fetch_flights_for_booking(self, booking_id: int):
        rows = self.db.query(
            """SELECT f.*
                FROM flights f
                JOIN bookings_flights bf ON bf.flight_id = f.id
                WHERE bf.booking_id = ?
            """,
            (booking_id,),
        ).fetchall()
        return [self.flights_repo._to_entity(row) for row in rows]

    def fetch_user_bookings(self, user_id: int) -> List["Booking"]:
        rows = self.db.query(
            """
            SELECT *
            FROM bookings b
            WHERE b.user_id = ?
            """,
            (user_id,),
        ).fetchall()
        return [self._to_entity(row) for row in rows]

    def fetch_booking_by_reference(self, reference: str) -> "Booking":
        row = self.db.query(
            """
            SELECT *
            FROM bookings b
            WHERE b.booking_reference = ?
            """,
            (reference,),
        ).fetchone()
        return self._to_entity(row)

    def save(self, booking: "Booking") -> "Booking":
        super().save(booking)
        for flight in booking.flights:
            self.db.execute(
                """
                INSERT INTO bookings_flights (booking_id, flight_id) VALUES (?, ?)
                """,
                (booking.id, flight.id),
            )
        return booking

    def _to_entity(self, row: Tuple) -> "Booking":
        from Flight_Project.entities.Booking import Booking

        user = self.users_repo.fetch_one(row[2])
        return Booking(
            id=row[0],
            booking_reference=row[1],
            user=user,
            number_of_passengers=row[3],
            total_amount=row[4],
            created_at=row[5],
        )

    def _to_tuple(self, booking: "Booking") -> Tuple[Any, ...]:
        return (
            booking.booking_reference,
            booking.user.id,
            booking.number_of_passengers,
            booking.total_amount,
            booking.created_at,
        )

    def _get_insert_columns(self) -> List[str]:
        return [
            "booking_reference",
            "user_id",
            "number_of_passengers",
            "total_amount",
            "created_at",
        ]
