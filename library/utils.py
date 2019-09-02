from config.settings import PROJECT_NAME, LOG_PATH
from library.service import t_logger
from functools import wraps
import time


logger = t_logger.get_module_logger(PROJECT_NAME, LOG_PATH)


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        r = func(*args, **kwargs)
        end = time.perf_counter()
        logger.debug('{}.{} : {}'.format(func.__module__, func.__name__, end - start))
        return r
    return wrapper
