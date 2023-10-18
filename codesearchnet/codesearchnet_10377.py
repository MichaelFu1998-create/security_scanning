def realpath(*args):
    """Join all args and return the real path, rooted at /.

    Expands ``~`` and environment variables such as :envvar:`$HOME`.

    Returns ``None`` if any of the args is none.
    """
    if None in args:
        return None
    return os.path.realpath(
        os.path.expandvars(os.path.expanduser(os.path.join(*args))))