import time

def timer(func):
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} completed in approximately {end - start:.2f} seconds")
        return result
    return inner

