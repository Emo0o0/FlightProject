from typing import Optional


class City:
    def __init__(
        self,
        name: str,
        id: Optional[int] = None,
    ):
        self.name = name
        self.id = id
