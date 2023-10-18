def SetWindowLong(handle: int, index: int, value: int) -> int:
    """
    SetWindowLong from Win32.
    handle: int, the handle of a native window.
    index: int.
    value: int.
    Return int, the previous value before set.
    """
    return ctypes.windll.user32.SetWindowLongW(ctypes.c_void_p(handle), index, value)