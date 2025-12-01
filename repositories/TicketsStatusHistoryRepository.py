import sqlite3

from Flight_Project.entities.TicketStatusHistory import TicketStatusHistory
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository


class TicketsStatusHistoryRepository(BaseRepository[TicketStatusHistory]):
    def __init__(self, db: RepositoryManager):
        self.db = db

    def create_table(self):
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS ticket_status_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticket_id INTEGER NOT NULL,
                    old_status TEXT,
                    new_status TEXT NOT NULL,
                    changed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (ticket_id) REFERENCES tickets(id)
                        ON UPDATE CASCADE ON DELETE CASCADE,
                    CHECK (new_status IN ('active','checked_in','boarded','cancelled','no_show'))
                )"""
        )
