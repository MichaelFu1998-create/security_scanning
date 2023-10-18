def GetWindowLong(handle: int, index: int) -> int:
    """
    GetWindowLong from Win32.
    handle: int, the handle of a native window.
    index: int.
    """
    return ctypes.windll.user32.GetWindowLongW(ctypes.c_void_p(handle), index)