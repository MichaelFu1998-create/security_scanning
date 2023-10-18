def SwitchToThisWindow(handle: int) -> None:
    """
    SwitchToThisWindow from Win32.
    handle: int, the handle of a native window.
    """
    ctypes.windll.user32.SwitchToThisWindow(ctypes.c_void_p(handle), 1)