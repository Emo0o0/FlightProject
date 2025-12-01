import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.User import User
from Flight_Project.repositories.CountriesRepository import CountriesRepository
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, db: RepositoryManager, countries_repo: CountriesRepository):
        super().__init__(db, "users")
        self.countries_repo = countries_repo

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    nationality_id INTEGER NOT NULL,
                    date_of_birth TEXT NOT NULL,
                    passport_number TEXT NOT NULL UNIQUE,
                    created_at DATE NOT NULL,
                    FOREIGN KEY (nationality_id) REFERENCES countries(id)
                        ON UPDATE CASCADE
                        ON DELETE RESTRICT
                )""",
            (),
        )

        self.db.execute(
            """CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)"""
        )

    def _to_entity(self, row: Tuple) -> User:
        country = self.countries_repo.fetch_one(row[6])
        return User(
            id=row[0],
            email=row[1],
            password=row[2],
            first_name=row[3],
            last_name=row[4],
            phone=row[5],
            nationality=country,
            date_of_birth=row[7],
            passport_number=row[8],
            created_at=row[9],
        )

    def _to_tuple(self, user: User) -> Tuple[Any, ...]:
        return (
            user.id,
            user.email,
            user.password,
            user.first_name,
            user.last_name,
            user.phone,
            user.nationality.id,
            user.date_of_birth,
            user.passport_number,
            user.created_at,
        )

    def _get_insert_columns(self) -> List[str]:
        return (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "nationality_id",
            "date_of_birth",
            "passport_number",
            "created_at",
        )
