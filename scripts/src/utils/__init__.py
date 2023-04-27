from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
# from sqlmodel import create_engine
import logging
import os
import sys
import uuid


try:
    __CONFIG = {
        "DB_HOST": os.environ["DB_HOST"],
        "DB_NAME": os.environ["DB_NAME"],
        "DB_PASS": os.environ["DB_PASS"],
        "DB_USER": os.environ["DB_USER"]
    }
except:
    raise Exception("Environment Variables Missing, Please Check Requirements in README")


def __create_database_engine() -> None:
    """
    Function for creating an sqlmodel Engine object to establish a connection with the database.

    Returns
    -------
    Engine - the sqlmodel Engine object
    """
    return None # create_engine(f"postgresql://{__CONFIG['DB_USER']}:{__CONFIG['DB_PASS']}@{__CONFIG['DB_HOST']}/{__CONFIG['DB_NAME']}")


def __create_logger() -> logging.Logger:
    """
    Function for creating a logger object to be used across the application.

    Returns
    -------
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


DATABASE: None = __create_database_engine()
LOGGER: logging.Logger = __create_logger()
