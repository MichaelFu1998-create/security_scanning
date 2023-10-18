def ensuredir(dpath, mode=0o1777, verbose=None):
    r"""
    Ensures that directory will exist. Creates new dir with sticky bits by
    default

    Args:
        dpath (PathLike): dir to ensure. Can also be a tuple to send to join
        mode (int): octal mode of directory (default 0o1777)
        verbose (int): verbosity (default 0)

    Returns:
        PathLike: path: the ensured directory

    Notes:
        This function is not thread-safe in Python2

    Example:
        >>> from ubelt.util_platform import *  # NOQA
        >>> import ubelt as ub
        >>> cache_dpath = ub.ensure_app_cache_dir('ubelt')
        >>> dpath = join(cache_dpath, 'ensuredir')
        >>> if exists(dpath):
        ...     os.rmdir(dpath)
        >>> assert not exists(dpath)
        >>> ub.ensuredir(dpath)
        >>> assert exists(dpath)
        >>> os.rmdir(dpath)
    """
    if verbose is None:  # nocover
        verbose = 0
    if isinstance(dpath, (list, tuple)):  # nocover
        dpath = join(*dpath)
    if not exists(dpath):
        if verbose:  # nocover
            print('Ensuring new directory (%r)' % dpath)
        if sys.version_info.major == 2:  # nocover
            os.makedirs(normpath(dpath), mode=mode)
        else:
            os.makedirs(normpath(dpath), mode=mode, exist_ok=True)
    else:
        if verbose:  # nocover
            print('Ensuring existing directory (%r)' % dpath)
    return dpath