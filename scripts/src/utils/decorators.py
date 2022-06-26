import time

def rate_limit(limit: int = 10, sec: int = 60):
    """
    Python-Decorator used to limit the number of calls to the decorated function over a given time period.
    Once the limit has been met, the thread will sleep until the time period has been completed.

    Parameters:
        - limit [int] - maximum number of calls to the function in the given time period
        - sec [int] - time period (in seconds)

    Example:
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
