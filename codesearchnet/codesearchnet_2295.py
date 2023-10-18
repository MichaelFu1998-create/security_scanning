def GetConsoleTitle() -> str:
    """
    GetConsoleTitle from Win32.
    Return str.
    """
    arrayType = ctypes.c_wchar * MAX_PATH
    values = arrayType()
    ctypes.windll.kernel32.GetConsoleTitleW(values, MAX_PATH)
    return values.value