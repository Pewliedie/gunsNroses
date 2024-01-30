from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .db import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    phone_number: Mapped[str]
    rank: Mapped[str]
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    active: Mapped[bool] = mapped_column(default=True)


class Fingerprint(Base):
    __tablename__ = 'fingerprints'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship(User)
    data: Mapped[str]
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class MaterialEvidence(Base):
    __tablename__ = 'material_evidence'

    id: Mapped[int] = mapped_column(primary_key=True)
    investigator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    investigator: Mapped[User] = relationship(User)
    description: Mapped[str]
    resolution: Mapped[str]
    status: Mapped[str]
    barcode: Mapped[int]
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
    active: Mapped[bool] = mapped_column(default=True)


class Audit(Base):
    __tablename__ = 'audits'

    id: Mapped[int] = mapped_column(primary_key=True)
    table: Mapped[str]
    previous_value: Mapped[str]
    new_value: Mapped[str]
    created: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped[User] = relationship(User)
