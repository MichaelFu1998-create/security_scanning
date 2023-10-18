def _find_resources(directory, excludes=[]):
    """Return a list of resource paths from the directory.
    Ignore records via the list of `excludes`,
    which are callables that take a file parameter (as a `Path` instance).

    """
    return sorted([r for r in directory.glob('*')
                   if True not in [e(r) for e in excludes]])