from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.Booking import Booking
    from entities.PaymentMethod import PaymentMethod


class Payment:
    def __init__(
        self,
        booking: "Booking",
        amount: float,
        payment_method: "PaymentMethod",
        paid_at: str,
        id: Optional[int] = None,
    ):
        self.id = id
        self.booking = booking
        self.amount = amount
        self.payment_method = payment_method
        self.paid_at = paid_at
