def backend():
    """
    :return:
        A unicode string of the backend being used: "openssl", "osx", "win",
        "winlegacy"
    """

    if _module_values['backend'] is not None:
        return _module_values['backend']

    with _backend_lock:
        if _module_values['backend'] is not None:
            return _module_values['backend']

        if sys.platform == 'win32':
            # Windows XP was major version 5, Vista was 6
            if sys.getwindowsversion()[0] < 6:
                _module_values['backend'] = 'winlegacy'
            else:
                _module_values['backend'] = 'win'
        elif sys.platform == 'darwin':
            _module_values['backend'] = 'osx'
        else:
            _module_values['backend'] = 'openssl'

        return _module_values['backend']