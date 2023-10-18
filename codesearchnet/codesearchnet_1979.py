def warnpy3k(message, category=None, stacklevel=1):
    """Issue a deprecation warning for Python 3.x related changes.

    Warnings are omitted unless Python is started with the -3 option.
    """
    if sys.py3kwarning:
        if category is None:
            category = DeprecationWarning
        warn(message, category, stacklevel+1)