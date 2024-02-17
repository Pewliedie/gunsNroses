import typing as t
from datetime import datetime

import src.models as m

from .base import BaseOutModel


class CaseListItem(BaseOutModel):
    id: int
    name: str
    investigator: str
    created: datetime
    updated: datetime

    @classmethod
    def from_obj(cls, obj: m.Case) -> t.Self:
        investigator = f"{obj.investigator.rank} - {obj.investigator.first_name} {obj.investigator.last_name}"
        data = {
            "id": obj.id,
            "name": obj.name,
            "investigator": investigator,
            "created": obj.created,
            "updated": obj.updated,
        }
        return cls(**data)

    def __str__(self) -> str:
        return f"{self.name} - {self.investigator}"


class CaseSelectItem(BaseOutModel):
    id: int
    name: str

    def __str__(self) -> str:
        return self.name


class CaseExportItem(BaseOutModel):
    id: int
    name: str
    investigator: str
    material_evidences: str
    created: datetime
    updated: datetime
    active: bool

    @classmethod
    def from_obj(cls, obj: m.Case) -> t.Self:
        investigator = f"{obj.investigator.first_name} {obj.investigator.last_name} - ({obj.investigator.rank})"
        material_evidences = "\n".join(
            [f"{e.name} - {e.status}" for e in obj.material_evidences]
        )
        data = {
            "id": obj.id,
            "name": obj.name,
            "investigator": investigator,
            "material_evidences": material_evidences,
            "created": obj.created,
            "updated": obj.updated,
            "active": obj.active,
        }
        return cls(**data)
