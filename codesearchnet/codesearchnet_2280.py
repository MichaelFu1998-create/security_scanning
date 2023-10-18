def GetAncestor(handle: int, flag: int) -> int:
    """
    GetAncestor from Win32.
    handle: int, the handle of a native window.
    index: int, a value in class `GAFlag`.
    Return int, a native window handle.
    """
    return ctypes.windll.user32.GetAncestor(ctypes.c_void_p(handle), flag)