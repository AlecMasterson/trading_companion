from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import logging
import os

API_BASE = None
Logger = None


if __name__ == "util":

    def __create_logger() -> logging.Logger:
        logger = logging.getLogger("main")
        logger.setLevel(logging.DEBUG)

        file_name = f"logs/{datetime.now().strftime('%Y-%m-%d-%H:%M:%S')}.log"
        formatter = logging.Formatter("[%(asctime)s] - [%(levelname)s] - %(message)s")

        for handler in [logging.FileHandler(file_name), logging.StreamHandler()]:
            handler.setLevel(logging.DEBUG)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    load_dotenv(find_dotenv(), verbose=True)
    API_BASE = os.environ.get("API_BASE")
    Logger = __create_logger()
