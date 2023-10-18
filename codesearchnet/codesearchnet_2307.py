def KeyboardInput(wVk: int, wScan: int, dwFlags: int = KeyboardEventFlag.KeyDown, time_: int = 0) -> INPUT:
    """Create Win32 struct `KEYBDINPUT` for `SendInput`."""
    return _CreateInput(KEYBDINPUT(wVk, wScan, dwFlags, time_, None))