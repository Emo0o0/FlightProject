from typing import Optional


class PaymentMethod:
    def __init__(
        self,
        id: Optional[int],
        method: str,
    ):
        self.id = id
        self.method = method
