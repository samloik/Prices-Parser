from functools import wraps
import time

from loguru import logger
from datetime import datetime

def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = datetime.now()
        result = func(*args, **kwargs)
        end_time = datetime.now()
        total_time = end_time - start_time
        logger.info(f'timeit: Функция {func.__name__}{args} {kwargs} выполнялась {total_time}')
        logger.info(f'timeit: Функция {func.__name__}{args} {kwargs} запушена {start_time}')
        logger.info(f'timeit: Функция {func.__name__}{args} {kwargs} выполнена {end_time}')
        return result
    return timeit_wrapper

# https://stackoverflow.com/questions/44169998/how-to-create-a-python-decorator-that-can-wrap-either-coroutine-or-function

import asyncio
import functools
import time
from contextlib import contextmanager


def duration(func):
    @contextmanager
    def wrapping_logic():
        start_time = time.time()
        yield
        end_time = time.time()
        total_time = end_time - start_time
        logger.info(f'timeit: Функция {func.__name__} выполнялась {total_time:.4} секунд')
        # logger.info(f'timeit: Функция {func.__name__} запушена {start_time}')
        # logger.info(f'timeit: Функция {func.__name__} выполнена {end_time}')
        # # print('{} took {:.2} seconds'.format(func.__name__, dur))

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            with wrapping_logic():
                return func(*args, **kwargs)
        else:
            async def tmp():
                with wrapping_logic():
                    return (await func(*args, **kwargs))
            return tmp()
    return wrapper


def duration2(func):
    @contextmanager
    def wrapping_logic():
        start_time = datetime.now()
        yield
        end_time = datetime.now()
        total_time = end_time - start_time
        logger.info(f'Функция {func.__name__} выполнялась {total_time}')
        logger.info(f'Функция {func.__name__} запушена {start_time}')
        logger.info(f'Функция {func.__name__} выполнена {end_time}')
        # # print('{} took {:.2} seconds'.format(func.__name__, dur))

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            with wrapping_logic():
                return func(*args, **kwargs)
        else:
            async def tmp():
                with wrapping_logic():
                    return (await func(*args, **kwargs))
            return tmp()
    return wrapper
