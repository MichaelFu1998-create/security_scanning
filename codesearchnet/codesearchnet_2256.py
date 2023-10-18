def WindowFromPoint(x: int, y: int) -> int:
    """
    WindowFromPoint from Win32.
    Return int, a native window handle.
    """
    return ctypes.windll.user32.WindowFromPoint(ctypes.wintypes.POINT(x, y))