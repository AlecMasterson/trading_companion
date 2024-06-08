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
        def wrapper_2(*args, **kwargs):
            limiter.increment()
            return func(*args, **kwargs)
        return wrapper_2

    return wrapper_1
