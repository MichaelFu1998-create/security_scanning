def trap(func):
    """
    Replace sys.std(out|err) with a wrapper during execution, restored after.

    In addition, a new combined-streams output (another wrapper) will appear at
    ``sys.stdall``. This stream will resemble what a user sees at a terminal,
    i.e. both out/err streams intermingled.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Use another CarbonCopy even though we're not cc'ing; for our "write
        # bytes, return strings on py3" behavior. Meh.
        sys.stdall = CarbonCopy()
        my_stdout, sys.stdout = sys.stdout, CarbonCopy(cc=sys.stdall)
        my_stderr, sys.stderr = sys.stderr, CarbonCopy(cc=sys.stdall)
        try:
            return func(*args, **kwargs)
        finally:
            sys.stdout = my_stdout
            sys.stderr = my_stderr
            del sys.stdall
    return wrapper