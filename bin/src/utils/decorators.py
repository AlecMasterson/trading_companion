from utils import LOGGER
import os
import psycopg
import time


def database_connection(func):
    def wrapper(*args, **kwargs):
        database: str = os.environ["POSTGRES_DB"]
        host: str = os.environ["POSTGRES_HOST"]
        password: str = os.environ["POSTGRES_PASSWORD"]
        port: str = os.environ["POSTGRES_PORT"]
        username: str = os.environ["POSTGRES_USER"]

        connection_string: str = f"dbname='{database}' user='{username}' host='{host}' port='{port}' password='{password}'"

        with psycopg.connect(connection_string) as connection:
            kwargs["database_conn"] = connection
            return func(*args, **kwargs)

    return wrapper


def rate_limit(limit: int = 10, sec: int = 60):
    """
    Python-Decorator used to limit the number of calls to the decorated function over a given time period.
    Once the limit has been met, the thread will sleep until the time period has been completed.

    Parameters
    ----------
    limit : int
        Maximum number of calls to the function in the given time period.
    sec : int
        Time period (in seconds).

    Example
    -------
    @rate_limit(limit=4, sec=30)
    def example_func():
        ...
    """
    class Limiter:
        def __init__(self, limit: int, sec: int):
            self.count = 0
            self.limit = limit
            self.sec = sec
            self.start = time.time()

        def increment(self):
            if self.count >= self.limit:
                time.sleep(max(0, self.sec - (time.time() - self.start)))
                self.count = 0
                self.start = time.time()
            self.count += 1

    limiter = Limiter(limit, sec)
    def wrapper_1(func):
        def rate_limit_wrapper(*args, **kwargs):
            limiter.increment()
            return func(*args, **kwargs)

        return rate_limit_wrapper

    return wrapper_1


def retry(delay: int = 5, num_retries: int = 3):
    def wrapper_1(func):
        log_prefix: str = f"retry_module=[{func.__module__}] - retry_func=[{func.__name__}]"
        def retry_wrapper(*args, **kwargs):
            attempt: int = 0
            while attempt < num_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt != num_retries:
                        LOGGER.warning(f"{log_prefix} - Error during attempt #{attempt+1}, waiting {delay}sec. Exception='{e}'")
                        time.sleep(delay)
                    attempt += 1
            raise Exception(f"{log_prefix} - Failed after {num_retries} attempts.")

        return retry_wrapper

    return wrapper_1
