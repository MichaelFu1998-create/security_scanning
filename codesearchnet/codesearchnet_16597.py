def _uptime_beos():
    """Returns uptime in seconds on None, on BeOS/Haiku."""
    try:
        libroot = ctypes.CDLL('libroot.so')
    except (AttributeError, OSError):
        return None

    if not hasattr(libroot, 'system_time'):
        return None

    libroot.system_time.restype = ctypes.c_int64
    return libroot.system_time() / 1000000.