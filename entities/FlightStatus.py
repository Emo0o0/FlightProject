from typing import Optional


class FlightStatus:
    def __init__(
        self,
        id: Optional[int],
        status: str,
    ):
        self.id = id
        self.status = status
