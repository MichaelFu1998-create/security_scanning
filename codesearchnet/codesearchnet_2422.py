def GetPixelColor(self, x: int, y: int) -> int:
        """
        Call native `GetPixelColor` if control has a valid native handle.
        Use `self.ToBitmap` if control doesn't have a valid native handle or you get many pixels.
        x: int, internal x position.
        y: int, internal y position.
        Return int, a color value in bgr.
        r = bgr & 0x0000FF
        g = (bgr & 0x00FF00) >> 8
        b = (bgr & 0xFF0000) >> 16
        """
        handle = self.NativeWindowHandle
        if handle:
            return GetPixelColor(x, y, handle)