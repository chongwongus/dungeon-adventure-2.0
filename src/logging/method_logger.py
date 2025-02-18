import functools

def debug_log_method_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Method called: {func.__name__} with args: {args} kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper
