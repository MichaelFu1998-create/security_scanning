def MessageBox(content: str, title: str, flags: int = MB.Ok) -> int:
    """
    MessageBox from Win32.
    content: str.
    title: str.
    flags: int, a value or some combined values in class `MB`.
    Return int, a value in MB whose name starts with Id, such as MB.IdOk
    """
    return ctypes.windll.user32.MessageBoxW(ctypes.c_void_p(0), ctypes.c_wchar_p(content), ctypes.c_wchar_p(title), flags)