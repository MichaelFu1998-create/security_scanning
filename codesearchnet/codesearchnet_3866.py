def touch(fpath, mode=0o666, dir_fd=None, verbose=0, **kwargs):
    """
    change file timestamps

    Works like the touch unix utility

    Args:
        fpath (PathLike): name of the file
        mode (int): file permissions (python3 and unix only)
        dir_fd (file): optional directory file descriptor. If specified, fpath
            is interpreted as relative to this descriptor (python 3 only).
        verbose (int): verbosity
        **kwargs : extra args passed to `os.utime` (python 3 only).

    Returns:
        PathLike: path to the file

    References:
        https://stackoverflow.com/questions/1158076/implement-touch-using-python

    Example:
        >>> import ubelt as ub
        >>> dpath = ub.ensure_app_cache_dir('ubelt')
        >>> fpath = join(dpath, 'touch_file')
        >>> assert not exists(fpath)
        >>> ub.touch(fpath)
        >>> assert exists(fpath)
        >>> os.unlink(fpath)
    """
    if verbose:
        print('Touching file {}'.format(fpath))
    if six.PY2:  # nocover
        with open(fpath, 'a'):
            os.utime(fpath, None)
    else:
        flags = os.O_CREAT | os.O_APPEND
        with os.fdopen(os.open(fpath, flags=flags, mode=mode, dir_fd=dir_fd)) as f:
            os.utime(f.fileno() if os.utime in os.supports_fd else fpath,
                     dir_fd=None if os.supports_fd else dir_fd, **kwargs)
    return fpath