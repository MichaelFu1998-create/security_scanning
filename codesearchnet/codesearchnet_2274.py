def GetScreenSize() -> tuple:
    """Return tuple, two ints tuple (width, height)."""
    SM_CXSCREEN = 0
    SM_CYSCREEN = 1
    w = ctypes.windll.user32.GetSystemMetrics(SM_CXSCREEN)
    h = ctypes.windll.user32.GetSystemMetrics(SM_CYSCREEN)
    return w, h