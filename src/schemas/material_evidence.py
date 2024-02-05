from datetime import datetime
from .base import BaseOutModel
import src.models as m


class MaterialEvidenceOut(BaseOutModel):
    id: int
    name: str
    case: str
    status: str
    created: datetime
    updated: datetime

    @classmethod
    def from_orm(cls, obj: m.MaterialEvidence):
        return cls(
            id=obj.id,
            name=obj.name,
            case=obj.case.name,
            status=obj.status,
            created=obj.created,
            updated=obj.updated,
        )
