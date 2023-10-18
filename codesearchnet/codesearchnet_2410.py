def MoveCursorToInnerPos(self, x: int = None, y: int = None, ratioX: float = 0.5, ratioY: float = 0.5, simulateMove: bool = True) -> tuple:
        """
        Move cursor to control's internal position, default to center.
        x: int, if < 0, move to self.BoundingRectangle.right + x, if not None, ignore ratioX.
        y: int, if < 0, move to self.BoundingRectangle.bottom + y, if not None, ignore ratioY.
        ratioX: float.
        ratioY: float.
        simulateMove: bool.
        Return tuple, two ints(x,y), the cursor positon relative to screen(0,0) after moving or None if control's width or height == 0.
        """
        rect = self.BoundingRectangle
        if rect.width() == 0 or rect.height() == 0:
            Logger.ColorfullyWriteLine('<Color=Yellow>Can not move curosr</Color>. {}\'s BoundingRectangle is {}. SearchProperties: {}'.format(
                self.ControlTypeName, rect, self.GetColorfulSearchPropertiesStr()))
            return
        if x is None:
            x = rect.left + int(rect.width() * ratioX)
        else:
            x = (rect.left if x >= 0 else rect.right) + x
        if y is None:
            y = rect.top + int(rect.height() * ratioY)
        else:
            y = (rect.top if y >= 0 else rect.bottom) + y
        if simulateMove and MAX_MOVE_SECOND > 0:
            MoveTo(x, y, waitTime=0)
        else:
            SetCursorPos(x, y)
        return x, y