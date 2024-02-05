from datetime import datetime
from .base import BaseOutModel
import src.models as m
import typing as t


class CaseOut(BaseOutModel):
    id: int
    investigator: str
    created: datetime
    updated: datetime

    @classmethod
    def from_obj(cls, obj: m.Case) -> t.Self:
        investigator = f'{obj.investigator.rank} - {obj.investigator.first_name} {obj.investigator.last_name}'
        data = {
            "id": obj.id,
            "investigator": investigator,
            "created": obj.created,
            "updated": obj.updated,
        }
        return cls(**data)
