def GetConsoleOriginalTitle() -> str:
    """
    GetConsoleOriginalTitle from Win32.
    Return str.
    Only available on Windows Vista or higher.
    """
    if IsNT6orHigher:
        arrayType = ctypes.c_wchar * MAX_PATH
        values = arrayType()
        ctypes.windll.kernel32.GetConsoleOriginalTitleW(values, MAX_PATH)
        return values.value
    else:
        raise RuntimeError('GetConsoleOriginalTitle is not supported on Windows XP or lower.')