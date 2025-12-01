from typing import Optional


class Country:
    def __init__(
        self,
        name: str,
        country_code: str,
        id: Optional[int] = None,
    ):
        self.id = id
        self.name = name
        self.country_code = country_code

    def __repr__(self):
        return f"Country(id={self.id}, name='{self.name}', country_code='{self.country_code}')"
