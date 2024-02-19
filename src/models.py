from datetime import datetime
from enum import Enum
from typing import List

from passlib.hash import pbkdf2_sha256
from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, desc, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression

from src.db import Base, session


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
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(
        default=datetime.now(), onupdate=datetime.now()
    )
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
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(
        default=datetime.now(), onupdate=datetime.now()
    )


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    investigator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    investigator: Mapped[User] = relationship(User, lazy="selectin")
    active: Mapped[bool] = mapped_column(default=True)
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(
        default=datetime.now(), onupdate=datetime.now()
    )
    material_evidences: Mapped[List["MaterialEvidence"]] = relationship(
        back_populates="case"
    )
    active: Mapped[bool] = mapped_column(server_default=expression.true())


class MaterialEvidenceStatus(Enum):
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
    description: Mapped[str]
    status = Column(
        SAEnum(MaterialEvidenceStatus),
        default=MaterialEvidenceStatus.IN_STORAGE,
        nullable=False,
    )
    barcode: Mapped[str]
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    updated: Mapped[datetime] = mapped_column(
        default=datetime.now(), onupdate=datetime.now()
    )
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
    created: Mapped[datetime] = mapped_column(default=datetime.now())


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(User)
    login: Mapped[datetime] = mapped_column(default=datetime.now())
    logout: Mapped[datetime | None] = mapped_column(onupdate=datetime.now())
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
    created: Mapped[datetime] = mapped_column(default=datetime.now())
    user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User | None] = relationship(User)
