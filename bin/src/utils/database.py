from sqlalchemy import Engine
from sqlmodel import Session, create_engine
from typing import Generator
import os

_database_name: str = os.environ["POSTGRES_DB"]
_database_host: str = os.environ["POSTGRES_HOST"]
_database_password: str = os.environ["POSTGRES_PASSWORD"]
_database_port: str = os.environ["POSTGRES_PORT"]
_database_user: str = os.environ["POSTGRES_USER"]
_engine: Engine = create_engine(
    f"postgresql://{_database_user}:{_database_password}@{_database_host}:{_database_port}/{_database_name}"
)

# TODO: is this really the best way to do database management?
def get_database_session() -> Generator[Session, None, None]:
    with Session(_engine) as database_session:
        yield database_session
