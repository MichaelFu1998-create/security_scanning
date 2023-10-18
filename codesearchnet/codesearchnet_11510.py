def last_arg_decorator(func):
    """
    Allows a function to be used as either a decorator with args, or called as
    a normal function.

    @last_arg_decorator
    def register_a_thing(foo, func, bar=True):
        ..

    # Called as a decorator
    @register_a_thing("abc", bar=False)
    def my_func():
        ...

    # Called as a normal function call
    def my_other_func():
        ...

    register_a_thing("def", my_other_func, bar=True)
    """
    @wraps(func)
    def decorator(*args, **kwargs):
        if signature_matches(func, args, kwargs):
            return func(*args, **kwargs)
        else:
            return lambda last: func(*(args + (last,)), **kwargs)
    return decorator