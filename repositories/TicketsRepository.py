import sqlite3

from Flight_Project.entities.Ticket import Ticket
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class TicketsRepository(BaseRepository[Ticket]):
    def __init__(self, db: RepositoryManager):
        self.db = db

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
