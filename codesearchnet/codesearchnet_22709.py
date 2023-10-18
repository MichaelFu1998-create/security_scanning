def _GetNativeEolStyle(platform=sys.platform):
    '''
    Internal function that determines EOL_STYLE_NATIVE constant with the proper value for the
    current platform.
    '''
    _NATIVE_EOL_STYLE_MAP = {
        'win32' : EOL_STYLE_WINDOWS,
        'linux2' : EOL_STYLE_UNIX,
        'linux' : EOL_STYLE_UNIX,
        'darwin' : EOL_STYLE_MAC,
    }
    result = _NATIVE_EOL_STYLE_MAP.get(platform)

    if result is None:
        from ._exceptions import UnknownPlatformError
        raise UnknownPlatformError(platform)

    return result