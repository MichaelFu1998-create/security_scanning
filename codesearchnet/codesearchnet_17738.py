def _wrapper(func):
    """
    Wraps a generated function so that it catches all Type- and ValueErrors
    and raises IntoDPValueErrors.

    :param func: the transforming function
    """

    @functools.wraps(func)
    def the_func(expr):
        """
        The actual function.

        :param object expr: the expression to be xformed to dbus-python types
        """
        try:
            return func(expr)
        except (TypeError, ValueError) as err:
            raise IntoDPValueError(expr, "expr", "could not be transformed") \
               from err

    return the_func