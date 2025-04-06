import time

class RateLimit:
    def __init__(self, limit: int = 1, seconds: int = 1):
        self.count = 0
        self.limit = limit
        self.seconds = seconds
        self.start = time.time()

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            if self.count >= self.limit:
                time.sleep(max(0, self.seconds - (time.time() - self.start)))
                self.count = 0
                self.start = time.time()

            self.count += 1
            return func(*args, **kwargs)
        return wrapper
