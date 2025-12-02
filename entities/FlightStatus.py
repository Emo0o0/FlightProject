from typing import Optional


class FlightStatus:
    def __init__(
        self,
        status: str,
        id: Optional[int] = None,
    ):
        self.id = id
        self.status = status
