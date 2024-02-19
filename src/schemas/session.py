import typing as t
from datetime import datetime

import src.models as m

from .base import BaseOutModel


class SessionListItem(BaseOutModel):
    id: int
    user: str
    login: datetime
    logout: datetime | None
    duration: float | None

    @classmethod
    def from_obj(cls, obj: m.Session) -> t.Self:
        user = f"{obj.user.rank} - {obj.user.last_name} {obj.user.first_name}"
        duration = (obj.logout - obj.login).total_seconds() if obj.logout else None
        data = {
            "id": obj.id,
            "user": user,
            "login": obj.login,
            "logout": obj.logout,
            "duration": duration,
        }
        return cls(**data)

    def __str__(self) -> str:
        return f"{self.user}"
    
class SessionExportItem(BaseOutModel):
        id: int
        user: str
        login: datetime
        logout: datetime | None
        duration: float | None

        @classmethod
        def from_obj(cls, obj: m.Session) -> t.Self:
            user = f"{obj.user.rank} - {obj.user.last_name} {obj.user.first_name}"
            duration = (obj.logout - obj.login).total_seconds() if obj.logout else None
            data = {
                "id": obj.id,
                "user": user,
                "login": obj.login,
                "logout": obj.logout,
                "duration": duration,
            }
            return cls(**data)