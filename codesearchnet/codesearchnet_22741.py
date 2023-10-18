def IsLink(path):
    '''
    :param unicode path:
        Path being tested

    :returns bool:
        True if `path` is a link
    '''
    _AssertIsLocal(path)

    if sys.platform != 'win32':
        return os.path.islink(path)

    import jaraco.windows.filesystem
    return jaraco.windows.filesystem.islink(path)