def MoveToCenter(self) -> bool:
        """
        Move window to screen center.
        """
        if self.IsTopLevel():
            rect = self.BoundingRectangle
            screenWidth, screenHeight = GetScreenSize()
            x, y = (screenWidth - rect.width()) // 2, (screenHeight - rect.height()) // 2
            if x < 0: x = 0
            if y < 0: y = 0
            return SetWindowPos(self.NativeWindowHandle, SWP.HWND_Top, x, y, 0, 0, SWP.SWP_NoSize)
        return False