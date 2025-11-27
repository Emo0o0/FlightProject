import sqlite3

from Flight_Project.repositories.RepositoryManager import RepositoryManager


class UserRepository:
    def __init__(self, db: RepositoryManager):
        self.db = db

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
