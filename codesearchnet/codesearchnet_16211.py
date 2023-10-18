def fluent(func):
    """Fluent interface decorator to return self if method return None."""
    @wraps(func)
    def fluent_interface(instance, *args, **kwargs):
        ret = func(instance, *args, **kwargs)
        if ret is not None:
            return ret
        return instance
    return fluent_interface