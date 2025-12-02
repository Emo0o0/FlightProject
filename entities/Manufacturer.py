from typing import Optional


class Manufacturer:
    def __init__(
        self,
        name: str,
        id: Optional[int] = None,
    ):
        self.id = id
        self.name = name
