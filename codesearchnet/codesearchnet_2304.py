def IsKeyPressed(key: int) -> bool:
    """
    key: int, a value in class `Keys`.
    Return bool.
    """
    state = ctypes.windll.user32.GetAsyncKeyState(key)
    return bool(state & 0x8000)