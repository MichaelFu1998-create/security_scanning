def SetWindowTopmost(handle: int, isTopmost: bool) -> bool:
    """
    handle: int, the handle of a native window.
    isTopmost: bool
    Return bool, True if succeed otherwise False.
    """
    topValue = SWP.HWND_Topmost if isTopmost else SWP.HWND_NoTopmost
    return bool(SetWindowPos(handle, topValue, 0, 0, 0, 0, SWP.SWP_NoSize | SWP.SWP_NoMove))