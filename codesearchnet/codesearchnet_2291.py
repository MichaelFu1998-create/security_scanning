def GetWindowText(handle: int) -> str:
    """
    GetWindowText from Win32.
    handle: int, the handle of a native window.
    Return str.
    """
    arrayType = ctypes.c_wchar * MAX_PATH
    values = arrayType()
    ctypes.windll.user32.GetWindowTextW(ctypes.c_void_p(handle), values, MAX_PATH)
    return values.value