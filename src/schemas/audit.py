import typing as t
from datetime import datetime

import src.models as m

from .base import BaseOutModel


class AuditEntryListItem(BaseOutModel):
    id: int
    object_id: int
    table_name: str
    class_name: str
    action: str
    fields: str
    data: str
    created: datetime
    user: str

    @classmethod
    def from_obj(cls, obj: m.AuditEntry) -> t.Self:
        user = (
            f"{obj.user.last_name} {obj.user.first_name} - ({obj.user.rank})"
            if obj.user
            else "Система"
        )
        data = {
            "id": obj.id,
            "object_id": obj.object_id,
            "table_name": obj.table_name,
            "class_name": obj.class_name,
            "action": obj.action,
            "fields": obj.fields,
            "data": obj.data,
            "created": obj.created,
            "user": user,
        }
        return cls(**data)
