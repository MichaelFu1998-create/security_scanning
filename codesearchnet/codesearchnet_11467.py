def mod_sys_path(paths):
    """
    A context manager that will append the specified paths to Python's
    ``sys.path`` during the execution of the block.

    :param paths: the paths to append
    :type paths: list(str)
    """

    old_path = sys.path
    sys.path = paths + sys.path
    try:
        yield
    finally:
        sys.path = old_path