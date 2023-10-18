def SetClipboardText(text: str) -> bool:
    """
    Return bool, True if succeed otherwise False.
    """
    if ctypes.windll.user32.OpenClipboard(0):
        ctypes.windll.user32.EmptyClipboard()
        textByteLen = (len(text) + 1) * 2
        hClipboardData = ctypes.windll.kernel32.GlobalAlloc(0, textByteLen)  # GMEM_FIXED=0
        hDestText = ctypes.windll.kernel32.GlobalLock(hClipboardData)
        ctypes.cdll.msvcrt.wcsncpy(ctypes.c_wchar_p(hDestText), ctypes.c_wchar_p(text), textByteLen // 2)
        ctypes.windll.kernel32.GlobalUnlock(hClipboardData)
        # system owns hClipboardData after calling SetClipboardData,
        # application can not write to or free the data once ownership has been transferred to the system
        ctypes.windll.user32.SetClipboardData(13, hClipboardData)  # CF_TEXT=1, CF_UNICODETEXT=13
        ctypes.windll.user32.CloseClipboard()
        return True
    return False