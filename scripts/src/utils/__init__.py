from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from sqlmodel import create_engine
from typing import List
import logging
import os
import sys
import uuid

def __create_database_engine():
    """
    Function for creating an Engine object to establish a connection with the database.
    4 different environment variables are required for connecting to the database.

    Returns:
        Engine - the sqlmodel engine object
    """
    details: List[str] = list(map(os.environ.get, ["DB_USER", "DB_PASS", "DB_HOST", "DB_NAME"]))
    return create_engine(f"postgresql://{details[0]}:{details[1]}@{details[2]}/{details[3]}")


def __create_logger() -> logging.Logger:
    """
    Function for creating a logger to be used across the application.
    The logger will write to the console and to a file (1 file per day).

    Returns:
        logging.Logger - the logger object
    """
    logger = logging.getLogger("main")
    logger.setLevel(logging.DEBUG)

    fileName = f"./logs/{datetime.now().strftime('%Y-%m-%d')}.log"
    fileFormatter = logging.Formatter("[%(asctime)s] - [%(levelname)s] - [" + str(uuid.uuid4()) + "] - [%(module)s] - [%(funcName)s] - %(message)s")

    fileHandler = TimedRotatingFileHandler(fileName, when="d", interval=1,  backupCount=5)
    fileHandler.setLevel(logging.INFO)
    fileHandler.setFormatter(fileFormatter)
    logger.addHandler(fileHandler)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    logger.addHandler(streamHandler)

    def exception_handler(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.exception("Uncaught Exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = exception_handler

    return logger

DATABASE = __create_database_engine()
LOGGER: logging.Logger = __create_logger()
