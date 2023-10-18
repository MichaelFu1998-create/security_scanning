def find_path(name, path=None, exact=False):
    """
    Search for a file or directory on your local filesystem by name
    (file must be in a directory specified in a PATH environment variable)

    Args:
        fname (PathLike or str): file name to match.
            If exact is False this may be a glob pattern

        path (str or Iterable[PathLike]): list of directories to search either
            specified as an os.pathsep separated string or a list of
            directories.  Defaults to environment PATH.

        exact (bool): if True, only returns exact matches. Default False.

    Notes:
        For recursive behavior set `path=(d for d, _, _ in os.walk('.'))`,
        where '.' might be replaced by the root directory of interest.

    Example:
        >>> list(find_path('ping', exact=True))
        >>> list(find_path('bin'))
        >>> list(find_path('bin'))
        >>> list(find_path('*cc*'))
        >>> list(find_path('cmake*'))

    Example:
        >>> import ubelt as ub
        >>> from os.path import dirname
        >>> path = dirname(dirname(ub.util_platform.__file__))
        >>> res = sorted(find_path('ubelt/util_*.py', path=path))
        >>> assert len(res) >= 10
        >>> res = sorted(find_path('ubelt/util_platform.py', path=path, exact=True))
        >>> print(res)
        >>> assert len(res) == 1
    """
    path = os.environ.get('PATH', os.defpath) if path is None else path
    dpaths = path.split(os.pathsep) if isinstance(path, six.string_types) else path
    candidates = (join(dpath, name) for dpath in dpaths)
    if exact:
        if WIN32:  # nocover
            pathext = [''] + os.environ.get('PATHEXT', '').split(os.pathsep)
            candidates = (p + ext for p in candidates for ext in pathext)
        candidates = filter(exists, candidates)
    else:
        import glob
        candidates = it.chain.from_iterable(
            glob.glob(pattern) for pattern in candidates)
    return candidates