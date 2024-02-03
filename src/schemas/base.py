from pydantic import BaseModel
from abc import ABC
from typing import Generic, Self, TypeVar

T = TypeVar("T")


class BaseOutModel(BaseModel, ABC, Generic[T]):
    @classmethod
    def from_obj(cls, obj: T) -> Self:
        return cls(**{field: getattr(obj, field) for field in cls.__fields__})
