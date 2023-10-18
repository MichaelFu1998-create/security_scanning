def Click(self, x: int = None, y: int = None, ratioX: float = 0.5, ratioY: float = 0.5, simulateMove: bool = True, waitTime: float = OPERATION_WAIT_TIME) -> None:
        """
        x: int, if < 0, click self.BoundingRectangle.right + x, if not None, ignore ratioX.
        y: int, if < 0, click self.BoundingRectangle.bottom + y, if not None, ignore ratioY.
        ratioX: float.
        ratioY: float.
        simulateMove: bool, if True, first move cursor to control smoothly.
        waitTime: float.

        Click(), Click(ratioX=0.5, ratioY=0.5): click center.
        Click(10, 10): click left+10, top+10.
        Click(-10, -10): click right-10, bottom-10.
        """
        point = self.MoveCursorToInnerPos(x, y, ratioX, ratioY, simulateMove)
        if point:
            Click(point[0], point[1], waitTime)