import typing as t
from datetime import datetime

from pydantic import BaseModel

import src.models as m

from .base import BaseOutModel


class MaterialEvidenceListItem(BaseModel):
    id: int
    name: str
    case: str
    status: str
    created: datetime
    updated: datetime

    @classmethod
    def from_obj(cls, obj: m.MaterialEvidence) -> t.Self:
        return cls(
            id=obj.id,
            name=obj.name,
            case=obj.case.name if obj.case else "",
            status=obj.status,
            created=obj.created,
            updated=obj.updated,
        )


class MaterialEvidenceSelectItem(BaseOutModel):
    id: int
    name: str
    status: str

    def __str__(self):
        return f"{self.name} - {self.status}"


class MaterialEvidenceExportItem(BaseOutModel):
    id: int
    name: str
    case: str
    status: str
    created: str
    updated: str
    active: str

    @classmethod
    def from_obj(cls, obj: m.MaterialEvidence) -> t.Self:
        data = {
            "id": obj.id,
            "name": obj.name,
            "case": obj.case.name if obj.case else "",
            "status": obj.status.value,
            "created": obj.created.strftime("%d/%m/%Y %H:%M:%S"),
            "updated": obj.updated.strftime("%d/%m/%Y %H:%M:%S"),
            "active": "Да" if obj.active else "Нет",
        }
        return cls(**data)
