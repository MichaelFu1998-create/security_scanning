def truepath(path, real=False):
    """
    Normalizes a string representation of a path and does shell-like expansion.

    Args:
        path (PathLike): string representation of a path
        real (bool): if True, all symbolic links are followed. (default: False)

    Returns:
        PathLike : normalized path

    Note:
        This function is similar to the composition of expanduser, expandvars,
        normpath, and (realpath if `real` else abspath). However, on windows
        backslashes are then replaced with forward slashes to offer a
        consistent unix-like experience across platforms.

        On windows expanduser will expand environment variables formatted as
        %name%, whereas on unix, this will not occur.

    CommandLine:
        python -m ubelt.util_path truepath

    Example:
        >>> import ubelt as ub
        >>> assert ub.truepath('~/foo') == join(ub.userhome(), 'foo')
        >>> assert ub.truepath('~/foo') == ub.truepath('~/foo/bar/..')
        >>> assert ub.truepath('~/foo', real=True) == ub.truepath('~/foo')
    """
    path = expanduser(path)
    path = expandvars(path)
    if real:
        path = realpath(path)
    else:
        path = abspath(path)
    path = normpath(path)
    return path