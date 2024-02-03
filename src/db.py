from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import DATABASE_PATH

# Create the engine with SQLite and specify the database file path
url = f'sqlite:///{DATABASE_PATH}'
engine = create_engine(url, echo=True)

# Create a session factory
Session = sessionmaker(bind=engine)
session = Session()


# Create a base class for declarative models
class Base(DeclarativeBase):
    pass


def init_db():
    Base.metadata.create_all(engine)
