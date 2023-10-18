def PressMouse(x: int, y: int, waitTime: float = OPERATION_WAIT_TIME) -> None:
    """
    Press left mouse.
    x: int.
    y: int.
    waitTime: float.
    """
    SetCursorPos(x, y)
    screenWidth, screenHeight = GetScreenSize()
    mouse_event(MouseEventFlag.LeftDown | MouseEventFlag.Absolute, x * 65535 // screenWidth, y * 65535 // screenHeight, 0, 0)
    time.sleep(waitTime)