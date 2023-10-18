def sizeClassifier(path, min_size=DEFAULTS['min_size']):
    """Sort a file into a group based on on-disk size.

    :param paths: See :func:`fastdupes.groupify`

    :param min_size: Files smaller than this size (in bytes) will be ignored.
    :type min_size: :class:`__builtins__.int`

    :returns: See :func:`fastdupes.groupify`

    .. todo:: Rework the calling of :func:`~os.stat` to minimize the number of
        calls. It's a fairly significant percentage of the time taken according
        to the profiler.
    """
    filestat = _stat(path)
    if stat.S_ISLNK(filestat.st_mode):
        return  # Skip symlinks.

    if filestat.st_size < min_size:
        return  # Skip files below the size limit

    return filestat.st_size