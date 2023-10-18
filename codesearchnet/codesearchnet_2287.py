def ShowWindow(handle: int, cmdShow: int) -> bool:
    """
    ShowWindow from Win32.
    handle: int, the handle of a native window.
    cmdShow: int, a value in clas `SW`.
    Return bool, True if succeed otherwise False.
    """
    return ctypes.windll.user32.ShowWindow(ctypes.c_void_p(handle), cmdShow)