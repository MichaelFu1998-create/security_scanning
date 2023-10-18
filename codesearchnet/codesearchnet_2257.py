def GetCursorPos() -> tuple:
    """
    GetCursorPos from Win32.
    Get current mouse cursor positon.
    Return tuple, two ints tuple (x, y).
    """
    point = ctypes.wintypes.POINT(0, 0)
    ctypes.windll.user32.GetCursorPos(ctypes.byref(point))
    return point.x, point.y