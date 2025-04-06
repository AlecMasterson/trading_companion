from logging import FileHandler
from typing import Any, Optional
from utils.date_util import get_now_eastern, to_string
import logging
import sys
import uuid

def __create_logger() -> logging.Logger:
    logger = logging.getLogger("main")
    logger.setLevel(logging.DEBUG)

    fileHandler = FileHandler(f"./logs/{to_string(get_now_eastern(), '%Y-%m-%d')}.log")
    fileHandler.setLevel(logging.INFO)
    fileHandler.setFormatter(logging.Formatter("[%(asctime)s] - level=[%(levelname)s] - trace=[" + str(uuid.uuid4()) + "] - module=[%(module)s] - func=[%(funcName)s] - %(message)s"))
    logger.addHandler(fileHandler)

    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)
    logger.addHandler(streamHandler)

    def exception_handler(exc_type: Optional[type], exc_value: Optional[BaseException], exc_traceback: Optional[Any]) -> None:
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        logger.exception("Uncaught Exception", exc_info=(exc_type, exc_value, exc_traceback))

    sys.excepthook = exception_handler

    return logger

LOGGER: logging.Logger = __create_logger()
