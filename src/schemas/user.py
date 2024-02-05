from datetime import datetime
from .base import BaseOutModel


class UserOut(BaseOutModel):
    id: int
    first_name: str
    last_name: str
    phone_number: str
    rank: str
    created: datetime
    updated: datetime
    active: bool

    def __str__(self):
        return f"{self.rank} - {self.first_name} {self.last_name}"
