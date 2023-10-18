def functional(ifunctional):
    """
    fun(fn) -> function or
    fun(fn, args...) -> call of fn(args...)
    :param ifunctional: f
    :return: decorated function
    """

    @wraps(ifunctional)
    def wrapper(fn, *args, **kw):

        fn = ifunctional(fn)
        if args or kw:
            return fn(*args, **kw)
        else:
            return fn

    return wrapper