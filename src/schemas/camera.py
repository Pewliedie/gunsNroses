from .base import BaseOutModel


class CameraListItem(BaseOutModel):
    id: int
    device_id: int
    name: str
    type: str
