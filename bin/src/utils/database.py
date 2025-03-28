from sqlalchemy import Engine
from sqlmodel import Session, create_engine
from typing import Generator
import os


engine: Engine = create_engine(f"postgresql://{os.environ['DB_USERNAME']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:5432/trading_companion")


# TODO: is this really the best way to do database management?
def get_database_session() -> Generator[Session, None, None]:
    with Session(engine) as database_session:
        yield database_session
