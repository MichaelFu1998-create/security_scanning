def find_exe(name, multi=False, path=None):
    """
    Locate a command.

    Search your local filesystem for an executable and return the first
    matching file with executable permission.

    Args:
        name (str): globstr of matching filename

        multi (bool): if True return all matches instead of just the first.
            Defaults to False.

        path (str or Iterable[PathLike]): overrides the system PATH variable.

    Returns:
        PathLike or List[PathLike] or None: returns matching executable(s).

    SeeAlso:
        shutil.which - which is available in Python 3.3+.

    Notes:
        This is essentially the `which` UNIX command

    References:
        https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python/377028#377028
        https://docs.python.org/dev/library/shutil.html#shutil.which

    Example:
        >>> find_exe('ls')
        >>> find_exe('ping')
        >>> assert find_exe('which') == find_exe(find_exe('which'))
        >>> find_exe('which', multi=True)
        >>> find_exe('ping', multi=True)
        >>> find_exe('cmake', multi=True)
        >>> find_exe('nvcc', multi=True)
        >>> find_exe('noexist', multi=True)

    Example:
        >>> assert not find_exe('noexist', multi=False)
        >>> assert find_exe('ping', multi=False)
        >>> assert not find_exe('noexist', multi=True)
        >>> assert find_exe('ping', multi=True)

    Benchmark:
        >>> # xdoctest: +IGNORE_WANT
        >>> import ubelt as ub
        >>> import shutil
        >>> for timer in ub.Timerit(100, bestof=10, label='ub.find_exe'):
        >>>     ub.find_exe('which')
        >>> for timer in ub.Timerit(100, bestof=10, label='shutil.which'):
        >>>     shutil.which('which')
        Timed best=58.71 탎, mean=59.64 � 0.96 탎 for ub.find_exe
        Timed best=72.75 탎, mean=73.07 � 0.22 탎 for shutil.which
    """
    candidates = find_path(name, path=path, exact=True)
    mode = os.X_OK | os.F_OK
    results = (fpath for fpath in candidates
               if os.access(fpath, mode) and not isdir(fpath))
    if not multi:
        for fpath in results:
            return fpath
    else:
        return list(results)