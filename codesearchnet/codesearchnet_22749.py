def ExpandUser(path):
    '''
    os.path.expanduser wrapper, necessary because it cannot handle unicode strings properly.

    This is not necessary in Python 3.

    :param path:
        .. seealso:: os.path.expanduser
    '''
    if six.PY2:
        encoding = sys.getfilesystemencoding()
        path = path.encode(encoding)
    result = os.path.expanduser(path)
    if six.PY2:
        result = result.decode(encoding)
    return result