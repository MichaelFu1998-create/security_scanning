def GetEditText(handle: int) -> str:
    """
    Get text of a native Win32 Edit.
    handle: int, the handle of a native window.
    Return str.
    """
    textLen = SendMessage(handle, 0x000E, 0, 0) + 1  #WM_GETTEXTLENGTH
    arrayType = ctypes.c_wchar * textLen
    values = arrayType()
    SendMessage(handle, 0x000D, textLen, values)  #WM_GETTEXT
    return values.value