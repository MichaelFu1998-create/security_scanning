def StandardizePath(path, strip=False):
    '''
    Replaces all slashes and backslashes with the target separator

    StandardPath:
        We are defining that the standard-path is the one with only back-slashes in it, either
        on Windows or any other platform.

    :param bool strip:
        If True, removes additional slashes from the end of the path.
    '''
    path = path.replace(SEPARATOR_WINDOWS, SEPARATOR_UNIX)
    if strip:
        path = path.rstrip(SEPARATOR_UNIX)
    return path