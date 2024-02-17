import typing as t
from datetime import datetime

import src.models as m

from .base import BaseOutModel


class UserListItem(BaseOutModel):
    id: int
    last_name: str
    first_name: str
    phone_number: str
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

    def __str__(self):
        return f"{self.last_name} {self.first_name} ({self.rank})"


class UserExportItem(BaseOutModel):
    id: int
    last_name: str
    first_name: str
    phone_number: str
    rank: str
    case_count: int
    created: datetime
    updated: datetime
    active: bool

    @classmethod
    def from_obj(cls, obj: m.User) -> t.Self:
        data = {
            "id": obj.id,
            "last_name": obj.last_name,
            "first_name": obj.first_name,
            "phone_number": obj.phone_number,
            "rank": obj.rank,
            "case_count": len(obj.cases),
            "created": obj.created,
            "updated": obj.updated,
            "active": obj.active,
        }
        return cls(**data)
