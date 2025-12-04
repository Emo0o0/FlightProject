import sqlite3
from typing import Any, List, Tuple

from Flight_Project.entities.TicketStatusHistory import TicketStatusHistory
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.BaseRepository import BaseRepository
from Flight_Project.repositories.TicketsRepository import TicketsRepository


class TicketsStatusHistoryRepository(BaseRepository[TicketStatusHistory]):
    def __init__(self, db: RepositoryManager, tickets_repo: TicketsRepository):
        super().__init__(db, "ticket_status_history")
        self.tickets_repo = tickets_repo

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

    def _to_entity(self, row: Tuple) -> TicketStatusHistory:
        ticket = self.tickets_repo.fetch_one(row[1])
        return TicketStatusHistory(
            id=row[0],
            ticket=ticket,
            old_status=row[2],
            new_status=row[3],
            changed_at=row[4],
            notes=row[5],
        )

    def _to_tuple(self, ticket_status_history: TicketStatusHistory) -> Tuple[Any, ...]:
        return (
            ticket_status_history.ticket.id,
            ticket_status_history.old_status,
            ticket_status_history.new_status,
            ticket_status_history.changed_at,
            ticket_status_history.notes,
        )

    def _get_insert_columns(self) -> List[str]:
        return [
            "ticket_id",
            "old_status",
            "new_status",
            "changed_at",
            "notes",
        ]
