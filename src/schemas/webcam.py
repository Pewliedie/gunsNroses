import typing as t
from datetime import datetime

import src.models as m

from .base import BaseOutModel

class WebCamListItem(BaseOutModel):
    id: int
    device_id: int
    name: str
    type: str
    
    @classmethod
    def from_obj(cls, obj: m.WebCam) -> t.Self:
        data = {
            "id": obj.id,
            "device_id": obj.device_id,
            "name": obj.name,
            "type": obj.type,
        }
        return cls(**data)