def removecallback(window_name):
    """
    Remove registered callback on window create

    @param window_name: Window name to look for, either full name,
    LDTP's name convention, or a Unix glob.
    @type window_name: string

    @return: 1 if registration was successful, 0 if not.
    @rtype: integer
    """

    if window_name in _pollEvents._callback:
        del _pollEvents._callback[window_name]
    return _remote_removecallback(window_name)