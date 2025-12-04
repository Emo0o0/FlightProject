import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.Ticket import Ticket
from Flight_Project.repositories.UsersRepository import UsersRepository
from Flight_Project.repositories.BookingsRepository import BookingsRepository
from Flight_Project.repositories.FlightsRepository import FlightsRepository
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class TicketsRepository(BaseRepository[Ticket]):
    def __init__(
        self,
        db: RepositoryManager,
        bookings_repo: BookingsRepository,
        flights_repo: FlightsRepository,
        users_repo: UsersRepository,
    ):
        super().__init__(db, "tickets")
        self.bookings_repo = bookings_repo
        self.flights_repo = flights_repo
        self.users_repo = users_repo

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS tickets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticket_number TEXT NOT NULL UNIQUE,
                    booking_id INTEGER NOT NULL,
                    flight_id INTEGER NOT NULL,
                    user_id INTEGER NOT NULL,
                    seat_number TEXT NOT NULL,
                    ticket_class TEXT NOT NULL CHECK(ticket_class IN ('economy','business','first-class')),
                    ticket_status TEXT NOT NULL CHECK(ticket_status IN ('active','checked_in','boarded','cancelled','no_show')),
                    issued_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    checked_in_at TIMESTAMP,
                    boarded_at TIMESTAMP,
                    cancelled_at TIMESTAMP,
                    no_show_at TIMESTAMP,
                    FOREIGN KEY (booking_id) REFERENCES bookings(id)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (flight_id) REFERENCES flights(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )"""
        )

        self.db.execute(
            """CREATE UNIQUE INDEX IF NOT EXISTS idx_tickets_ticket_number ON tickets(ticket_number)"""
        )

    def fetch_user_tickets(self, user_id):
        rows = self.db.query(
            """
            SELECT *
            FROM tickets t
            WHERE t.user_id = ?
            """,
            (user_id,),
        ).fetchall()
        return [self._to_entity(row) for row in rows]

    def _to_entity(self, row: Tuple) -> Ticket:
        booking = self.bookings_repo.fetch_one(row[2])
        flight = self.flights_repo.fetch_one(row[3])
        user = self.users_repo.fetch_one(row[4])
        return Ticket(
            id=row[0],
            ticket_number=row[1],
            booking=booking,
            flight=flight,
            user=user,
            seat_number=row[5],
            ticket_class=row[6],
            ticket_status=row[7],
            issued_at=row[8],
            checked_in_at=row[9],
            boarded_at=row[10],
            cancelled_at=row[11],
            no_show_at=row[12],
        )

    def _to_tuple(self, ticket: Ticket) -> Tuple[Any, ...]:
        return (
            ticket.ticket_number,
            ticket.booking.id,
            ticket.flight.id,
            ticket.user.id,
            ticket.seat_number,
            ticket.ticket_class,
            ticket.ticket_status,
            ticket.issued_at,
            ticket.checked_in_at,
            ticket.boarded_at,
            ticket.cancelled_at,
            ticket.no_show_at,
        )

    def _get_insert_columns(self) -> List[str]:
        return [
            "ticket_number",
            "booking_id",
            "flight_id",
            "user_id",
            "seat_number",
            "ticket_class",
            "ticket_status",
            "issued_at",
            "checked_in_at",
            "boarded_at",
            "cancelled_at",
            "no_show_at",
        ]
