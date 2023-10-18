def timeout_handler(interval, recurring = None):
    """Method decorator generator for decorating event handlers.

    To be used on `TimeoutHandler` subclass methods only.

    :Parameters:
        - `interval`: interval (in seconds) before the method will be called.
        - `recurring`: When `True`, the handler will be called each `interval`
          seconds, when `False` it will be called only once. If `True`,
          then the handler should return the next interval or `None` if it
          should not be called again.
    :Types:
        - `interval`: `float`
        - `recurring`: `bool`
    """
    def decorator(func):
        """The decorator"""
        func._pyxmpp_timeout = interval
        func._pyxmpp_recurring = recurring
        return func
    return decorator