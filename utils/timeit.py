from time import time


def timeit(func):
    def wrapper_function(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        print(f"{func.__name__!r} took {(end - start)}s")
        return result

    return wrapper_function
