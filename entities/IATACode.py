from typing import Optional


class IATACode:
    def __init__(
        self,
        code: str,
        id: Optional[int] = None,
    ):
        self.id = id
        self.code = code
