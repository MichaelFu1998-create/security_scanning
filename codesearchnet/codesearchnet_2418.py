def MoveWindow(self, x: int, y: int, width: int, height: int, repaint: bool = True) -> bool:
        """
        Call native MoveWindow if control has a valid native handle.
        x: int.
        y: int.
        width: int.
        height: int.
        repaint: bool.
        Return bool, True if succeed otherwise False.
        """
        handle = self.NativeWindowHandle
        if handle:
            return MoveWindow(handle, x, y, width, height, int(repaint))
        return False