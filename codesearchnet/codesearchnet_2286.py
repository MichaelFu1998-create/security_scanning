def IsWindowVisible(handle: int) -> bool:
    """
    IsWindowVisible from Win32.
    handle: int, the handle of a native window.
    Return bool.
    """
    return bool(ctypes.windll.user32.IsWindowVisible(ctypes.c_void_p(handle)))