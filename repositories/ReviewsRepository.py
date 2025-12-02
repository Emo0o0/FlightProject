import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.Review import Review
from Flight_Project.repositories.FlightsRepository import FlightsRepository
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository
from Flight_Project.repositories.UsersRepository import UserRepository


class ReviewsRepository(BaseRepository[Review]):
    def __init__(
        self,
        db: RepositoryManager,
        users_repo: UserRepository,
        flights_repo: FlightsRepository,
    ):
        self.db = db
        self.users_repo = users_repo
        self.flights_repo = flights_repo

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

    def _to_entity(self, row: Tuple) -> Review:
        user = self.users_repo.fetch_one(row[1])
        flight = self.flights_repo.fetch_one(row[2])
        return Review(
            id=row[0],
            user=user,
            flight=flight,
            description=row[3],
            created_at=row[4],
        )

    def _to_tuple(self, review: Review) -> Tuple[Any, ...]:
        return (
            review.id,
            review.user.id,
            review.flight.id,
            review.description,
            review.created_at,
        )

    def _get_insert_columns(self) -> List[str]:
        return ["id", "user_id", "flight_id", "description", "created_at"]
