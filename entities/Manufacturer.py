from typing import Optional


class Manufacturer:
    def __init__(
        self,
        id: Optional[int],
        name: str,
    ):
        self.id = id
        self.name = name
