def platform_config_dir():
    """
    Returns a directory which should be writable for any application
    This should be used for persistent configuration files.

    Returns:
        PathLike : path to the cahce dir used by the current operating system
    """
    if LINUX:  # nocover
        dpath_ = os.environ.get('XDG_CONFIG_HOME', '~/.config')
    elif DARWIN:  # nocover
        dpath_  = '~/Library/Application Support'
    elif WIN32:  # nocover
        dpath_ = os.environ.get('APPDATA', '~/AppData/Roaming')
    else:  # nocover
        raise NotImplementedError('Unknown Platform  %r' % (sys.platform,))
    dpath = normpath(expanduser(dpath_))
    return dpath