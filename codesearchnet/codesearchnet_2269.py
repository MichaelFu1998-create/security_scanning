def RightReleaseMouse(waitTime: float = OPERATION_WAIT_TIME) -> None:
    """
    Release right mouse.
    waitTime: float.
    """
    x, y = GetCursorPos()
    screenWidth, screenHeight = GetScreenSize()
    mouse_event(MouseEventFlag.RightUp | MouseEventFlag.Absolute, x * 65535 // screenWidth, y * 65535 // screenHeight, 0, 0)
    time.sleep(waitTime)