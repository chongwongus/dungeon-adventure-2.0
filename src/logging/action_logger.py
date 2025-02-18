import functools

def log_action_method_call(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Configuration called: {func.__name__} with args: {args} kwargs: {kwargs}")
        return func(*args, **kwargs)
    return wrapper
