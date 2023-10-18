def _GetFileAndLine():
    """Returns (filename, linenumber) for the stack frame."""
    # Use sys._getframe().  This avoids creating a traceback object.
    # pylint: disable=protected-access
    f = _sys._getframe()
    # pylint: enable=protected-access
    our_file = f.f_code.co_filename
    f = f.f_back
    while f:
        code = f.f_code
        if code.co_filename != our_file:
            return (code.co_filename, f.f_lineno)
        f = f.f_back
    return ('<unknown>', 0)