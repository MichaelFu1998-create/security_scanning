def HardwareInput(uMsg: int, param: int = 0) -> INPUT:
    """Create Win32 struct `HARDWAREINPUT` for `SendInput`."""
    return _CreateInput(HARDWAREINPUT(uMsg, param & 0xFFFF, param >> 16 & 0xFFFF))