import time


def timer(func: callable):
    """
    计时器装饰器
    """

    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Func - {func.__name__} - Time taken: {(end_time - start_time):.4f}sec")
        return result

    return wrapper
