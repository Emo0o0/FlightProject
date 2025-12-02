from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.Ticket import Ticket


class TicketStatusHistory:
    def __init__(
        self,
        ticket: "Ticket",
        old_status: str,
        new_status: str,
        changed_at: str,
        notes: str,
        id: Optional[int] = None,
    ):
        self.id = id
        self.ticket = ticket
        self.old_status = old_status
        self.new_status = new_status
        self.changed_at = changed_at
        self.notes = notes
