def print_exception(etype, value, tb, limit=None, file=None):
    """Print exception up to 'limit' stack trace entries from 'tb' to 'file'.

    This differs from print_tb() in the following ways: (1) if
    traceback is not None, it prints a header "Traceback (most recent
    call last):"; (2) it prints the exception type and value after the
    stack trace; (3) if type is SyntaxError and value has the
    appropriate format, it prints the line where the syntax error
    occurred with a caret on the next line indicating the approximate
    position of the error.
    """
    if file is None:
        # TODO: Use sys.stderr when that's implemented.
        file = open('/dev/stderr', 'w')
        #file = sys.stderr
    if tb:
        _print(file, 'Traceback (most recent call last):')
        print_tb(tb, limit, file)
    lines = format_exception_only(etype, value)
    for line in lines:
        _print(file, line, '')