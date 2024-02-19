import typing as t
from datetime import datetime

import src.models as m

from .base import BaseOutModel


def seconds_to_human_readable(seconds):
    days = round(seconds // (24 * 3600))
    hours = round((seconds % (24 * 3600)) // 3600)
    minutes = round((seconds % 3600) // 60)
    seconds = round(seconds % 60)

    result = ""
    if days > 0:
        result += f"{days}дн. "
    if hours > 0:
        result += f"{hours}ч. "
    if minutes > 0:
        result += f"{minutes}м. "
    if seconds > 0:
        result += f"{seconds}c."

    return result.strip(', ')


class SessionListItem(BaseOutModel):
    id: int
    user: str
    login: datetime
    logout: datetime | None
    duration: str | None

    @classmethod
    def from_obj(cls, obj: m.Session) -> t.Self:
        user = f"{obj.user.last_name} {obj.user.first_name} - ({obj.user.rank})"
        duration = (
            seconds_to_human_readable((obj.logout - obj.login).total_seconds())
            if obj.logout
            else None
        )
        data = {
            "id": obj.id,
            "user": user,
            "login": obj.login,
            "logout": obj.logout,
            "duration": duration,
        }
        return cls(**data)
