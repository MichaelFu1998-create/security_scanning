def _uptime_windows():
    """
    Returns uptime in seconds or None, on Windows. Warning: may return
    incorrect answers after 49.7 days on versions older than Vista.
    """
    if hasattr(ctypes, 'windll') and hasattr(ctypes.windll, 'kernel32'):
        lib = ctypes.windll.kernel32
    else:
        try:
            # Windows CE uses the cdecl calling convention.
            lib = ctypes.CDLL('coredll.lib')
        except (AttributeError, OSError):
            return None

    if hasattr(lib, 'GetTickCount64'):
        # Vista/Server 2008 or later.
        lib.GetTickCount64.restype = ctypes.c_uint64
        return lib.GetTickCount64() / 1000.
    if hasattr(lib, 'GetTickCount'):
        # WinCE and Win2k or later; gives wrong answers after 49.7 days.
        lib.GetTickCount.restype = ctypes.c_uint32
        return lib.GetTickCount() / 1000.
    return None