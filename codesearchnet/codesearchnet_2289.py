def SetWindowPos(handle: int, hWndInsertAfter: int, x: int, y: int, width: int, height: int, flags: int) -> bool:
    """
    SetWindowPos from Win32.
    handle: int, the handle of a native window.
    hWndInsertAfter: int, a value whose name starts with 'HWND' in class SWP.
    x: int.
    y: int.
    width: int.
    height: int.
    flags: int, values whose name starts with 'SWP' in class `SWP`.
    Return bool, True if succeed otherwise False.
    """
    return ctypes.windll.user32.SetWindowPos(ctypes.c_void_p(handle), ctypes.c_void_p(hWndInsertAfter), x, y, width, height, flags)