from datetime import datetime
from .base import BaseOutModel
import src.models as m
import typing as t


class CaseListItem(BaseOutModel):
    id: int
    name: str
    investigator: str
    created: datetime
    updated: datetime

    @classmethod
    def from_obj(cls, obj: m.Case) -> t.Self:
        investigator = f'{obj.investigator.rank} - {obj.investigator.first_name} {obj.investigator.last_name}'
        data = {
            "id": obj.id,
            "name": obj.name,
            "investigator": investigator,
            "created": obj.created,
            "updated": obj.updated,
        }
        return cls(**data)

    def __str__(self) -> str:
        return f'{self.name} - {self.investigator}'


class CaseSelectItem(BaseOutModel):
    id: int
    name: str

    def __str__(self) -> str:
        return self.name
