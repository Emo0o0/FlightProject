from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from entities.Country import Country


class User:
    def __init__(
        self,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        phone: str,
        nationality: "Country",
        date_of_birth: str,
        passport_number: str,
        created_at: str,
        id: Optional[int] = None,
    ):
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.nationality = nationality
        self.date_of_birth = date_of_birth
        self.passport_number = passport_number
        self.created_at = created_at

    def __repr__(self):
        return f"User: id = {self.id}, name = {self.first_name} {self.last_name}"
