def SetWindowText(handle: int, text: str) -> bool:
    """
    SetWindowText from Win32.
    handle: int, the handle of a native window.
    text: str.
    Return bool, True if succeed otherwise False.
    """
    return bool(ctypes.windll.user32.SetWindowTextW(ctypes.c_void_p(handle), ctypes.c_wchar_p(text)))