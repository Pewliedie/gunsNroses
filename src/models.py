from datetime import datetime
from enum import StrEnum
from time import time
from typing import List

from passlib.hash import pbkdf2_sha256
from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from src.db import Base, session


def default_now():
    return datetime.now()


def create_barcode_value():
    return round(time())


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    password_hash: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    rank: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(server_default=expression.false())
    active: Mapped[bool] = mapped_column(server_default=expression.true())
    created: Mapped[datetime] = mapped_column(default=default_now)
    updated: Mapped[datetime] = mapped_column(default=default_now, onupdate=default_now)
    cases: Mapped[List["Case"]] = relationship(
        "Case", back_populates="investigator", lazy="selectin"
    )
    face: Mapped["FaceID"] = relationship("FaceID", back_populates="user")
    active: Mapped[bool] = mapped_column(server_default=expression.true())

    def set_password(self, password):
        self.password_hash = pbkdf2_sha256.hash(password)

    def check_password(self, password):
        return pbkdf2_sha256.verify(password, self.password_hash)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - ({self.rank})"


class FaceID(Base):
    __tablename__ = "face_ids"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="face")
    data: Mapped[str]
    created: Mapped[datetime] = mapped_column(default=default_now)
    updated: Mapped[datetime] = mapped_column(default=default_now, onupdate=default_now)


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    investigator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    investigator: Mapped[User] = relationship(User, lazy="selectin")
    active: Mapped[bool] = mapped_column(default=True)
    created: Mapped[datetime] = mapped_column(default=default_now)
    updated: Mapped[datetime] = mapped_column(default=default_now, onupdate=default_now)
    material_evidences: Mapped[List["MaterialEvidence"]] = relationship(
        back_populates="case"
    )
    active: Mapped[bool] = mapped_column(server_default=expression.true())


class MaterialEvidenceStatus(StrEnum):
    IN_STORAGE = "На хранении"
    DESTROYED = "Уничтожен"
    TAKEN = "Взят"
    ON_EXAMINATION = "На экспертизе"
    ARCHIVED = "В архиве"


class MaterialEvidence(Base):
    __tablename__ = "material_evidences"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    case_id: Mapped[int | None] = mapped_column(ForeignKey("cases.id"))
    case: Mapped[Case | None] = relationship(
        Case, back_populates="material_evidences", lazy="selectin"
    )
    created_by_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_by: Mapped[User] = relationship(User)
    description: Mapped[str]
    status = Column(
        SAEnum(MaterialEvidenceStatus),
        default=MaterialEvidenceStatus.IN_STORAGE,
        nullable=False,
    )
    barcode: Mapped[str] = mapped_column(default=create_barcode_value)
    created: Mapped[datetime] = mapped_column(default=default_now)
    updated: Mapped[datetime] = mapped_column(default=default_now, onupdate=default_now)
    active: Mapped[bool] = mapped_column(server_default=expression.true())

    @property
    def last_event(self):
        query = (
            select(MaterialEvidenceEvent)
            .filter(MaterialEvidenceEvent.material_evidence_id == self.id)
            .order_by(MaterialEvidenceEvent.created.desc())
        )
        last_event = session.scalars(query).first()
        return last_event


class MaterialEvidenceEvent(Base):
    __tablename__ = "material_evidence_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(User)
    material_evidence_id: Mapped[int] = mapped_column(
        ForeignKey("material_evidences.id")
    )
    material_evidence: Mapped[MaterialEvidence] = relationship(MaterialEvidence)
    action = Column(SAEnum(MaterialEvidenceStatus), nullable=False)
    created: Mapped[datetime] = mapped_column(default=default_now)


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(User)
    login: Mapped[datetime] = mapped_column(default=default_now)
    logout: Mapped[datetime | None] = mapped_column(onupdate=default_now)
    active: Mapped[bool] = mapped_column(server_default=expression.true())


class CameraType(StrEnum):
    FACE_ID = "Аутентификация по лицу"
    REC = "Запись видео"
    DEFAULT = "Обычная камера"


class Camera(Base):
    __tablename__ = "cameras"

    id: Mapped[int] = mapped_column(primary_key=True)
    device_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str]
    type: Mapped[str] = mapped_column(SAEnum(CameraType))
    created: Mapped[datetime] = mapped_column(default=default_now)
    updated: Mapped[datetime] = mapped_column(default=default_now, onupdate=default_now)
    active: Mapped[bool] = mapped_column(server_default=expression.true())


class AuditEntry(Base):
    __tablename__ = "audit_entries"

    id: Mapped[int] = mapped_column(primary_key=True)
    object_id: Mapped[int]
    table_name: Mapped[str]
    class_name: Mapped[str]
    action: Mapped[str]
    fields: Mapped[str]
    data: Mapped[str]
    created: Mapped[datetime] = mapped_column(default=default_now)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User | None] = relationship(User)
