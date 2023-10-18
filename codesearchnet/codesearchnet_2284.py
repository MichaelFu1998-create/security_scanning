def IsIconic(handle: int) -> bool:
    """
    IsIconic from Win32.
    Determine whether a native window is minimized.
    handle: int, the handle of a native window.
    Return bool.
    """
    return bool(ctypes.windll.user32.IsIconic(ctypes.c_void_p(handle)))