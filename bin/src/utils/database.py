from sqlalchemy import Engine
from sqlmodel import Session, create_engine
from typing import Generator
import os

engine: Engine = create_engine(os.environ["POSTGRES_CONN_STR"])

# TODO: is this really the best way to do database management?
def get_database_session() -> Generator[Session, None, None]:
    with Session(engine) as database_session:
        yield database_session
