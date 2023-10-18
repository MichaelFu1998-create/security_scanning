def ReadLink(path):
    '''
    Read the target of the symbolic link at `path`.

    :param unicode path:
        Path to a symbolic link

    :returns unicode:
        Target of a symbolic link
    '''
    _AssertIsLocal(path)

    if sys.platform != 'win32':
        return os.readlink(path)  # @UndefinedVariable

    if not IsLink(path):
        from ._exceptions import FileNotFoundError
        raise FileNotFoundError(path)

    import jaraco.windows.filesystem
    result = jaraco.windows.filesystem.readlink(path)
    if '\\??\\' in result:
        result = result.split('\\??\\')[1]
    return result