from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.User import User
    from entities.Flight import Flight


class Review:
    def __init__(
        self,
        user: "User",
        flight: "Flight",
        rating: int,
        description: str,
        created_at: str,
        id: Optional[int] = None,
    ):
        self.id = id
        self.user = user
        self.flight = flight
        self.rating = rating
        self.description = description
        self.created_at = created_at
