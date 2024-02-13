import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.sql import text

from .config import DEBUG, DATABASE_PATH


def casefold(s: str):
    return s.casefold()


# Create the engine with SQLite and specify the database file path
url = f"sqlite:///{DATABASE_PATH}"
engine = create_engine(url, echo=DEBUG)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()


@sa.event.listens_for(sa.engine.Engine, "connect")
def sqlite_engine_connect(connection, _):
    connection.create_function("casefold", 1, casefold)


# Create a base class for declarative models
class Base(DeclarativeBase):
    pass


def init_db():
    Base.metadata.create_all(engine)
