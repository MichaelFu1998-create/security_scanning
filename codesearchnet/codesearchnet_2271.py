def DragDrop(x1: int, y1: int, x2: int, y2: int, moveSpeed: float = 1, waitTime: float = OPERATION_WAIT_TIME) -> None:
    """
    Simulate mouse left button drag from point x1, y1 drop to point x2, y2.
    x1: int.
    y1: int.
    x2: int.
    y2: int.
    moveSpeed: float, 1 normal speed, < 1 move slower, > 1 move faster.
    waitTime: float.
    """
    PressMouse(x1, y1, 0.05)
    MoveTo(x2, y2, moveSpeed, 0.05)
    ReleaseMouse(waitTime)