import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.Payment import Payment
from Flight_Project.repositories.BookingsRepository import BookingsRepository
from Flight_Project.repositories.PaymentMethodsRepository import (
    PaymentMethodsRepository,
)
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class PaymentsRepository(BaseRepository[Payment]):
    def __init__(
        self,
        db: RepositoryManager,
        bookings_repo: BookingsRepository,
        payment_methods_repo: PaymentMethodsRepository,
    ):
        self.db = db
        self.bookings_repo = bookings_repo
        self.payment_methods_repo = payment_methods_repo

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

    def _to_entity(self, row: Tuple) -> Payment:
        booking = self.bookings_repo.fetch_one(row[1])
        payment_method = self.payment_methods_repo.fetch_one(row[3])
        return Payment(
            id=row[0],
            booking=booking,
            amount=row[2],
            payment_method=payment_method,
            paid_at=row[4],
        )

    def _to_tuple(self, payment: Payment) -> Tuple[Any, ...]:
        return (
            payment.id,
            payment.booking.id,
            payment.amount,
            payment.payment_method.id,
            payment.paid_at,
        )

    def _get_insert_columns(self) -> List[str]:
        return ["id", "booking_id", "amount", "payment_method_id", "paid_at"]
