def SetConsoleTitle(text: str) -> bool:
    """
    SetConsoleTitle from Win32.
    text: str.
    Return bool, True if succeed otherwise False.
    """
    return bool(ctypes.windll.kernel32.SetConsoleTitleW(ctypes.c_wchar_p(text)))