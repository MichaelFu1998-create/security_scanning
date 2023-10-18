def platform_data_dir():
    """
    Returns path for user-specific data files

    Returns:
        PathLike : path to the data dir used by the current operating system
    """
    if LINUX:  # nocover
        dpath_ = os.environ.get('XDG_DATA_HOME', '~/.local/share')
    elif DARWIN:  # nocover
        dpath_  = '~/Library/Application Support'
    elif WIN32:  # nocover
        dpath_ = os.environ.get('APPDATA', '~/AppData/Roaming')
    else:  # nocover
        raise '~/AppData/Local'
    dpath = normpath(expanduser(dpath_))
    return dpath