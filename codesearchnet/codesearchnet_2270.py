def MoveTo(x: int, y: int, moveSpeed: float = 1, waitTime: float = OPERATION_WAIT_TIME) -> None:
    """
    Simulate mouse move to point x, y from current cursor.
    x: int.
    y: int.
    moveSpeed: float, 1 normal speed, < 1 move slower, > 1 move faster.
    waitTime: float.
    """
    if moveSpeed <= 0:
        moveTime = 0
    else:
        moveTime = MAX_MOVE_SECOND / moveSpeed
    curX, curY = GetCursorPos()
    xCount = abs(x - curX)
    yCount = abs(y - curY)
    maxPoint = max(xCount, yCount)
    screenWidth, screenHeight = GetScreenSize()
    maxSide = max(screenWidth, screenHeight)
    minSide = min(screenWidth, screenHeight)
    if maxPoint > minSide:
        maxPoint = minSide
    if maxPoint < maxSide:
        maxPoint = 100 + int((maxSide - 100) / maxSide * maxPoint)
        moveTime = moveTime * maxPoint * 1.0 / maxSide
    stepCount = maxPoint // 20
    if stepCount > 1:
        xStep = (x - curX) * 1.0 / stepCount
        yStep = (y - curY) * 1.0 / stepCount
        interval = moveTime / stepCount
        for i in range(stepCount):
            cx = curX + int(xStep * i)
            cy = curY + int(yStep * i)
            # upper-left(0,0), lower-right(65536,65536)
            # mouse_event(MouseEventFlag.Move | MouseEventFlag.Absolute, cx*65536//screenWidth, cy*65536//screenHeight, 0, 0)
            SetCursorPos(cx, cy)
            time.sleep(interval)
    SetCursorPos(x, y)
    time.sleep(waitTime)