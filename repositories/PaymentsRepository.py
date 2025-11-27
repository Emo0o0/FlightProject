import sqlite3

from Flight_Project.repositories.RepositoryManager import RepositoryManager


class PaymentsRepository:
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS payments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    booking_id INTEGER NOT NULL,
                    amount REAL NOT NULL,
                    payment_method_id INTEGER NOT NULL,
                    paid_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (booking_id) REFERENCES bookings(id)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (payment_method_id) REFERENCES payment_methods(id)
                        ON UPDATE CASCADE ON DELETE RESTRICT
                )"""
        )
