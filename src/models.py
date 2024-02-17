from datetime import datetime

import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import expression, func
from typing import List
from src.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    password: Mapped[str]
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    rank: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(server_default=expression.false())
    active: Mapped[bool] = mapped_column(default=True)

    created: Mapped[datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    face: Mapped["FaceID"] = relationship("FaceID", back_populates="user")
    active: Mapped[bool] = mapped_column(server_default=expression.true())


class FaceID(Base):
    __tablename__ = "face_ids"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    data: Mapped[str]

    created: Mapped[datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="face")


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(primary_key=True)
    investigator_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    investigator: Mapped[User] = relationship(User, lazy="selectin")
    name: Mapped[str]
    description: Mapped[str]
    active: Mapped[bool] = mapped_column(default=True)

    created: Mapped[datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    material_evidences: Mapped[List["MaterialEvidence"]] = relationship(
        back_populates="case"
    )
    active: Mapped[bool] = mapped_column(server_default=expression.true())


class MaterialEvidence(Base):
    __tablename__ = "material_evidence"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    case_id: Mapped[int | None] = mapped_column(ForeignKey("cases.id"))
    case: Mapped[Case | None] = relationship(
        Case, back_populates="material_evidences", lazy="selectin"
    )
    description: Mapped[str]
    status: Mapped[str]
    barcode: Mapped[int]
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    active: Mapped[bool] = mapped_column(server_default=expression.true())

class MaterialEvidenceEvent(Base):
    __tablename__ = "material_evidence_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(User)
    material_evidence_id: Mapped[int] = mapped_column(ForeignKey("material_evidence.id"))
    material_evidence: Mapped[MaterialEvidence] = relationship(MaterialEvidence)
    event_type: Mapped[str]
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    active: Mapped[bool] = mapped_column(server_default=expression.true())


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(User)
    login: Mapped[datetime] = mapped_column(server_default=func.now())
    logout: Mapped[datetime | None] = mapped_column(onupdate=func.now())
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
    created: Mapped[datetime] = mapped_column(server_default=sa.func.now())
    # user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    # user: Mapped[User] = relationship(User)
