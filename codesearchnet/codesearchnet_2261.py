def PostMessage(handle: int, msg: int, wParam: int, lParam: int) -> bool:
    """
    PostMessage from Win32.
    Return bool, True if succeed otherwise False.
    """
    return bool(ctypes.windll.user32.PostMessageW(ctypes.c_void_p(handle), msg, wParam, lParam))