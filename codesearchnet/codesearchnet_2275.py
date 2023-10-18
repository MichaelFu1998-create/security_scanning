def GetPixelColor(x: int, y: int, handle: int = 0) -> int:
    """
    Get pixel color of a native window.
    x: int.
    y: int.
    handle: int, the handle of a native window.
    Return int, the bgr value of point (x,y).
    r = bgr & 0x0000FF
    g = (bgr & 0x00FF00) >> 8
    b = (bgr & 0xFF0000) >> 16
    If handle is 0, get pixel from Desktop window(root control).
    Note:
    Not all devices support GetPixel.
    An application should call GetDeviceCaps to determine whether a specified device supports this function.
    For example, console window doesn't support.
    """
    hdc = ctypes.windll.user32.GetWindowDC(ctypes.c_void_p(handle))
    bgr = ctypes.windll.gdi32.GetPixel(hdc, x, y)
    ctypes.windll.user32.ReleaseDC(ctypes.c_void_p(handle), hdc)
    return bgr