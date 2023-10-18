def MiddleClick(x: int, y: int, waitTime: float = OPERATION_WAIT_TIME) -> None:
    """
    Simulate mouse middle click at point x, y.
    x: int.
    y: int.
    waitTime: float.
    """
    SetCursorPos(x, y)
    screenWidth, screenHeight = GetScreenSize()
    mouse_event(MouseEventFlag.MiddleDown | MouseEventFlag.Absolute, x * 65535 // screenWidth, y * 65535 // screenHeight, 0, 0)
    time.sleep(0.05)
    mouse_event(MouseEventFlag.MiddleUp | MouseEventFlag.Absolute, x * 65535 // screenWidth, y * 65535 // screenHeight, 0, 0)
    time.sleep(waitTime)