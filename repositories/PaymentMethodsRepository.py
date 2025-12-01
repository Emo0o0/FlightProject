import sqlite3

from Flight_Project.entities.PaymentMethod import PaymentMethod
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class PaymentMethodsRepository(BaseRepository[PaymentMethod]):
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS payment_methods (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    method TEXT NOT NULL UNIQUE
                )"""
        )
