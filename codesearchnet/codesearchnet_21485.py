def get_or_default(func=None, default=None):
    """
    Wrapper around Django's ORM `get` functionality.
    Wrap anything that raises ObjectDoesNotExist exception
    and provide the default value if necessary.
    `default` by default is None. `default` can be any callable,
    if it is callable it will be called when ObjectDoesNotExist
    exception will be raised.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ObjectDoesNotExist:
                if callable(default):
                    return default()
                else:
                    return default
        return wrapper
    if func is None:
        return decorator
    else:
        return decorator(func)