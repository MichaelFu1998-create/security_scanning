def keybd_event(bVk: int, bScan: int, dwFlags: int, dwExtraInfo: int) -> None:
    """keybd_event from Win32."""
    ctypes.windll.user32.keybd_event(bVk, bScan, dwFlags, dwExtraInfo)