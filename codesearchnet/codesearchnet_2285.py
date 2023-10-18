def IsZoomed(handle: int) -> bool:
    """
    IsZoomed from Win32.
    Determine whether a native window is maximized.
    handle: int, the handle of a native window.
    Return bool.
    """
    return bool(ctypes.windll.user32.IsZoomed(ctypes.c_void_p(handle)))