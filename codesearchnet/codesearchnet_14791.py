def opt_args_decorator(func):
    """A decorator to be used on another decorator

    This is done to allow separate handling on the basis of argument values
    """
    @wraps(func)
    def wrapped_dec(*args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0 and callable(args[0]):
            # actual decorated function
            return func(args[0])
        else:
            # decorator arguments
            return lambda realf: func(realf, *args, **kwargs)

    return wrapped_dec