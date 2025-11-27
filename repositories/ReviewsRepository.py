import sqlite3

from Flight_Project.repositories.RepositoryManager import RepositoryManager


class ReviewsRepository:
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    flight_id INTEGER NOT NULL,
                    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
                    description TEXT,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    FOREIGN KEY (flight_id) REFERENCES flights(id)
                        ON UPDATE CASCADE ON DELETE CASCADE
                )"""
        )
