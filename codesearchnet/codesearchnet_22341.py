def settings(path=None, with_path=None):
    """
    Get or set `Settings._wrapped`

    :param str path: a python module file,
        if user set it,write config to `Settings._wrapped`
    :param str with_path: search path
    :return: A instance of `Settings`
    """

    if path:
        Settings.bind(path, with_path=with_path)

    return Settings._wrapped