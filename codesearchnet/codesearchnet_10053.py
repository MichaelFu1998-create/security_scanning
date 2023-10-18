def _is_osx_107():
    """
    :return:
        A bool if the current machine is running OS X 10.7
    """

    if sys.platform != 'darwin':
        return False
    version = platform.mac_ver()[0]
    return tuple(map(int, version.split('.')))[0:2] == (10, 7)