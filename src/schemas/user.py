from datetime import datetime

from .base import BaseOutModel


class UserListItem(BaseOutModel):
    id: int
    last_name: str
    first_name: str
    phone_number: str
    password: str
    rank: str
    created: datetime
    updated: datetime

    def __str__(self):
        return f"{self.rank} - {self.last_name} {self.first_name}"


class UserSelectItem(BaseOutModel):
    id: int
    last_name: str
    first_name: str
    rank: str
    password: str

    def __str__(self):
        return f"{self.rank} - {self.last_name} {self.first_name}"
