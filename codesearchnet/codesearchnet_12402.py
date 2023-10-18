def redirect_stdout(new_stdout):
    """Redirect the stdout

    Args:
        new_stdout (io.StringIO): New stdout to use instead
    """
    old_stdout, sys.stdout = sys.stdout, new_stdout
    try:
        yield None
    finally:
        sys.stdout = old_stdout