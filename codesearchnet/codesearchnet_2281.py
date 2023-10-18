def IsTopLevelWindow(handle: int) -> bool:
    """
    IsTopLevelWindow from Win32.
    handle: int, the handle of a native window.
    Return bool.
    Only available on Windows 7 or Higher.
    """
    return bool(ctypes.windll.user32.IsTopLevelWindow(ctypes.c_void_p(handle)))