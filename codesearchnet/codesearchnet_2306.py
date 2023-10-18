def MouseInput(dx: int, dy: int, mouseData: int = 0, dwFlags: int = MouseEventFlag.LeftDown, time_: int = 0) -> INPUT:
    """
    Create Win32 struct `MOUSEINPUT` for `SendInput`.
    Return `INPUT`.
    """
    return _CreateInput(MOUSEINPUT(dx, dy, mouseData, dwFlags, time_, None))