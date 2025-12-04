import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.PaymentMethod import PaymentMethod
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class PaymentMethodsRepository(BaseRepository[PaymentMethod]):
    def __init__(self, db: RepositoryManager):
        super().__init__(db, "payment_methods")

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS payment_methods (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    method TEXT NOT NULL UNIQUE
                )"""
        )

    def _to_entity(self, row: Tuple) -> PaymentMethod:
        return PaymentMethod(
            id=row[0],
            method=row[1],
        )

    def _to_tuple(self, payment_method: PaymentMethod) -> Tuple[Any, ...]:
        return (payment_method.method,)

    def _get_insert_columns(self) -> List[str]:
        return [
            "method",
        ]
