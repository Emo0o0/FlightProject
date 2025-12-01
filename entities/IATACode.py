from typing import Optional


class IATACode:
    def __init__(
        self,
        id: Optional[int],
        code: str,
    ):
        self.id = id
        self.code = code
