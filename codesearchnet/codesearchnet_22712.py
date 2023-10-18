def CanonicalPath(path):
    '''
    Returns a version of a path that is unique.

    Given two paths path1 and path2:
        CanonicalPath(path1) == CanonicalPath(path2) if and only if they represent the same file on
        the host OS. Takes account of case, slashes and relative paths.

    :param unicode path:
        The original path.

    :rtype: unicode
    :returns:
        The unique path.
    '''
    path = os.path.normpath(path)
    path = os.path.abspath(path)
    path = os.path.normcase(path)

    return path