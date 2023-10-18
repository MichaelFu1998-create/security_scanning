def WheelDown(self, wheelTimes: int = 1, interval: float = 0.05, waitTime: float = OPERATION_WAIT_TIME) -> None:
        """
        Make control have focus first, move cursor to center and mouse wheel down.
        wheelTimes: int.
        interval: float.
        waitTime: float.
        """
        x, y = GetCursorPos()
        self.SetFocus()
        self.MoveCursorToMyCenter(False)
        WheelDown(wheelTimes, interval, waitTime)
        SetCursorPos(x, y)