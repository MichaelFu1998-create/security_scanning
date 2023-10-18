def capture_stdout():
    """This ``Context Manager`` redirects STDOUT to a ``StringIO`` objects
    which is returned from the ``Context``.  On exit STDOUT is restored.

    Example:

    .. code-block:: python

        with capture_stdout() as capture:
            print('foo')

        # got here? => capture.getvalue() will now have "foo\\n"
    """
    stdout = sys.stdout
    try:
        capture_out = StringIO()
        sys.stdout = capture_out
        yield capture_out
    finally:
        sys.stdout = stdout