from utils import LOGGER
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
