from typing import Optional


class PaymentMethod:
    def __init__(
        self,
        method: str,
        id: Optional[int] = None,
    ):
        self.id = id
        self.method = method
