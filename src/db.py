import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import DEBUG, DATABASE_PATH


def casefold(s: str):
    return s.casefold()


url = f"sqlite:///{DATABASE_PATH}"
engine = create_engine(url, echo=DEBUG)


Session = sessionmaker(bind=engine)
session = Session()


@sa.event.listens_for(sa.engine.Engine, "connect")
def sqlite_engine_connect(connection, _):
    connection.create_function("casefold", 1, casefold)


class Base(DeclarativeBase):
    pass


def init_db():
    Base.metadata.create_all(engine)
