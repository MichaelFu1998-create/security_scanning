def compressuser(path, home='~'):
    """
    Inverse of `os.path.expanduser`

    Args:
        path (PathLike): path in system file structure
        home (str): symbol used to replace the home path. Defaults to '~', but
            you might want to use '$HOME' or '%USERPROFILE%' instead.

    Returns:
        PathLike: path: shortened path replacing the home directory with a tilde

    CommandLine:
        xdoctest -m ubelt.util_path compressuser

    Example:
        >>> path = expanduser('~')
        >>> assert path != '~'
        >>> assert compressuser(path) == '~'
        >>> assert compressuser(path + '1') == path + '1'
        >>> assert compressuser(path + '/1') == join('~', '1')
        >>> assert compressuser(path + '/1', '$HOME') == join('$HOME', '1')
    """
    path = normpath(path)
    userhome_dpath = userhome()
    if path.startswith(userhome_dpath):
        if len(path) == len(userhome_dpath):
            path = home
        elif path[len(userhome_dpath)] == os.path.sep:
            path = home + path[len(userhome_dpath):]
    return path