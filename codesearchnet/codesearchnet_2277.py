def SetForegroundWindow(handle: int) -> bool:
    """
    SetForegroundWindow from Win32.
    handle: int, the handle of a native window.
    Return bool, True if succeed otherwise False.
    """
    return bool(ctypes.windll.user32.SetForegroundWindow(ctypes.c_void_p(handle)))