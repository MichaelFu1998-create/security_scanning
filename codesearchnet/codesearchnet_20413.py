def capture_stderr():
    """This ``Context Manager`` redirects STDERR to a ``StringIO`` objects
    which is returned from the ``Context``.  On exit STDERR is restored.

    Example:

    .. code-block:: python

        with capture_stderr() as capture:
            print('foo')

        # got here? => capture.getvalue() will now have "foo\\n"
    """
    stderr = sys.stderr
    try:
        capture_out = StringIO()
        sys.stderr = capture_out
        yield capture_out
    finally:
        sys.stderr = stderr