from datetime import datetime
from .base import BaseOutModel


class CaseOut(BaseOutModel):
    id: int
    investigator_id: int
    description: str
    created: datetime
    updated: datetime
    active: bool
