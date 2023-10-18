def DoubleClick(self, x: int = None, y: int = None, ratioX: float = 0.5, ratioY: float = 0.5, simulateMove: bool = True, waitTime: float = OPERATION_WAIT_TIME) -> None:
        """
        x: int, if < 0, right click self.BoundingRectangle.right + x, if not None, ignore ratioX.
        y: int, if < 0, right click self.BoundingRectangle.bottom + y, if not None, ignore ratioY.
        ratioX: float.
        ratioY: float.
        simulateMove: bool, if True, first move cursor to control smoothly.
        waitTime: float.

        DoubleClick(), DoubleClick(ratioX=0.5, ratioY=0.5): double click center.
        DoubleClick(10, 10): double click left+10, top+10.
        DoubleClick(-10, -10): double click right-10, bottom-10.
        """
        x, y = self.MoveCursorToInnerPos(x, y, ratioX, ratioY, simulateMove)
        Click(x, y, GetDoubleClickTime() * 1.0 / 2000)
        Click(x, y, waitTime)