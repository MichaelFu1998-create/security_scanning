def SendMessage(handle: int, msg: int, wParam: int, lParam: int) -> int:
    """
    SendMessage from Win32.
    Return int, the return value specifies the result of the message processing;
                it depends on the message sent.
    """
    return ctypes.windll.user32.SendMessageW(ctypes.c_void_p(handle), msg, wParam, lParam)